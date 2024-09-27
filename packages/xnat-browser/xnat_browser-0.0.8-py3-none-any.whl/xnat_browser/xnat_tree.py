import enum
import http
import logging
import re
from dataclasses import dataclass
from typing import Any

import xnat
from rich.text import Text
from textual import work
from textual.binding import Binding
from textual.message import Message
from textual.widgets import Tree, Label
from textual.widgets.tree import TreeNode
from xnat.core import XNATListing
from xnat.exceptions import XNATResponseError
from xnat.mixin import ImageScanData, ProjectData, SubjectData, ImageSessionData
from xnat.prearchive import PrearchiveScan, PrearchiveSession

from xnat_browser.app_base import Loading
from xnat_browser.dicom_highlighter import DicomHighlighter
from xnat_browser.image_viewer import ImageViewer

MAX_NAME_LENGTH = 25


# XNAT does not have a PrearchiveSubject, so define it here.
@dataclass
class PrearchiveSubject:
    # Used as a placeholder incase the subject does not (yet) exist.
    name: str


class Views(enum.Enum):
    XNAT_INFO = enum.auto()
    DICOM_INFO = enum.auto()
    DICOM_IMAGE = enum.auto()


@dataclass
class Outputs:
    xnat: Label
    dicom: Label
    image: ImageViewer

    def clear(self) -> None:
        self.xnat.update('')
        self.dicom.update('')
        self.image.set_image(None)


class XnatTree(Tree):
    class ViewChanged(Message):
        def __init__(self, view: Views):
            super().__init__()
            self.view = view

    BINDINGS = [
        Binding('left', 'goto_parent', 'Goto Parent', show=False),
    ]

    def __init__(self, outputs: Outputs, logger: logging.Logger, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.outputs = outputs
        self.logger = logger
        self.show_root = False
        self.session: xnat.XNATSession | None = None
        self._last_processed_dicom: TreeNode | None = None

    def set_session(self, session: xnat.XNATSession) -> None:
        raise NotImplementedError()

    def access_level(self) -> dict:
        # copied from https://gitlab.com/radiology/infrastructure/xnatpy/-/commit/d0e32c669a0cb2bda0f2c8b828d80470510f1c7b
        assert self.session
        data: list[dict[str, Any]] = self.session.get_json('/xapi/access/projects')
        result = {}
        for x in data:
            if 'ID' not in x or 'role' not in x:
                continue
            result[x['ID']] = x['role']
        return result

    def action_goto_parent(self) -> None:
        node = self.cursor_node
        if node is None or node.parent is None:
            return

        self.select_node(node.parent)
        self.scroll_to_node(node.parent)

    async def filter_projects(self, _: str) -> None:
        raise NotImplementedError()

    async def action_refresh(self) -> None:
        raise NotImplementedError()

    def action_update_projects(self) -> None:
        raise NotImplementedError()

    def dicom_info(self) -> None:
        node = self.cursor_node
        if node is None or node == self._last_processed_dicom:
            return

        with Loading(self.outputs.xnat):
            self.logger.debug('DICOM action')
            self._last_processed_dicom = node
            if isinstance(node.data, (ImageScanData, PrearchiveScan)):
                try:
                    self.outputs.image.set_xnat_data(node.data)
                    self.outputs.dicom.update(DicomHighlighter()(str(self.outputs.image.dicom_data)))
                except XNATResponseError as e:
                    status = _get_http_status_code(e)
                    if status == http.HTTPStatus.FORBIDDEN:
                        self.logger.error("you don't have permission to access this resource.")
                        return
                    self.logger.error(f'Error downloading dicom file. {e}')
                except ValueError as e:
                    self.logger.error(f'Error {e}')

    @work(thread=True)
    def _process_node(self, node: TreeNode) -> None:
        match node.data:
            case ProjectData():
                if len(node.children) > 0:
                    return
                _add(node, node.data.subjects, ' SUB')

            case SubjectData():
                if len(node.children) > 0:
                    return
                _add(node, node.data.experiments, ' EXP')  # type: ignore

            case ImageSessionData():
                if len(node.children) > 0:
                    return
                scans = node.data.scans  # type: ignore
                node.set_label(Text(f'[{len(scans):>3} SCN] {node.label}'))
                for scan in scans.values():  # type: ignore
                    node.add_leaf(scan.type, scan)

            case PrearchiveSession():
                if len(node.children) > 0:
                    return
                if node.data.status != 'READY':
                    return
                scans = node.data.scans  # type: ignore
                node.set_label(Text(f'[{len(scans):>3} SCN] {node.label}'))
                for scan in scans:  # type: ignore
                    label = scan.series_description if len(scan.series_description) > 0 else scan.id
                    node.add_leaf(label, scan)

            case PrearchiveSubject():
                # See if the subject already exists in this project. If so, add the SubjectData to the node
                assert node.parent
                project_data = node.parent.data
                assert isinstance(project_data, ProjectData)

                xnat_subject = _get_subject(project_data, str(node.label))
                if xnat_subject:
                    node.data = xnat_subject


def _get_subject(project: ProjectData, name: str) -> SubjectData | None:
    subjects: list[SubjectData] = list(filter(lambda x: x.label == name, project.subjects.values()))
    return subjects[0] if len(subjects) > 0 else None


def _add(node: TreeNode, data: XNATListing, suffix: str = "") -> None:
    label_re = r'.*\] (?P<label>.*)$'

    label = node.label
    m = re.search(label_re, str(label))
    if m:
        label = m.group('label')
    node.set_label(Text(f'[{len(data):>4}{suffix}] {label}'))

    for key in sorted(x.label for x in data.values()):
        value = data[key]
        node.add(value.label, value)


def _get_http_status_code(e: Exception) -> int:
    match = re.search(r'status (?P<status_code>\d{3})', str(e), flags=re.S)
    if not match:
        return -1

    return int(match.group("status_code"))
