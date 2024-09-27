import logging
import math
from typing import Any, cast, Final

import xnat
from rich.text import Text
from textual import work, on
from textual.widgets import Tree
from textual.worker import WorkerCancelled
from xnat.mixin import ProjectData

from xnat_browser.app_base import Loading
from xnat_browser.create_markdown import create_markdown
from xnat_browser.xnat_tree import XnatTree, MAX_NAME_LENGTH, Outputs, Views

ARCHIVE_NODE_ID: Final[str] = 'archive'


class XnatArchiveTree(XnatTree):  # pylint: disable=too-many-ancestors
    def __init__(self, outputs: Outputs, logger: logging.Logger, **kwargs: Any) -> None:
        super().__init__(label='xnat_archive_tree', outputs=outputs, logger=logger, **kwargs)
        self.outputs = outputs
        self.logger = logger
        self.show_root = False
        self.session: xnat.XNATSession | None = None

    def set_session(self, session: xnat.XNATSession) -> None:
        self.logger.debug('Updating archive tree')
        self.session = session
        with Loading(self):
            # noinspection PyArgumentList
            self._add_projects()
        self.root.expand()

    @work(thread=True)
    def _add_projects(self) -> None:
        assert self.session
        self.logger.debug('Adding archive projects')

        allowed_projects = self.access_level().keys()

        # sort the projects using case-insensitive sorting.
        for project in sorted(self.session.projects.values(), key=lambda x: x.name.casefold()):  # type: ignore
            name = project.name
            if name not in allowed_projects:
                continue
            if len(name) > MAX_NAME_LENGTH:
                name = name[:MAX_NAME_LENGTH - 3] + '...'
            self.root.add(name, project)
        self.root.expand()
        self.root.set_label(Text(f'[{len(self.root.children):>2}] Archive'))

    async def action_refresh(self) -> None:
        assert self.session

        node = self.cursor_node

        with Loading(self):
            self.session.clearcache()

            if node is None or node == self.root:
                self.root.remove_children()
                self.logger.debug('Refreshing archive root')
                # noinspection PyArgumentList
                self._add_projects()
                return

            self.logger.debug(f'Refreshing archive "{node.label}"')
            node.remove_children()
            self._process_node(node)
            return

    @work(thread=True)
    def action_update_projects(self) -> None:  # type: ignore
        self.logger.debug('Updating projects')
        with Loading(self):
            proj_dict = {}

            # make a copy of the children because the iterator becomes invalid on node removal.
            for project_node in list(self.root.children):
                num_subjects = len(cast(ProjectData, project_node.data).subjects)
                if num_subjects == 0:
                    project_node.remove()
                    continue
                proj_dict[project_node] = num_subjects

            max_subjects = max(proj_dict.values())
            num_digits = int(math.log10(max_subjects)) + 1

            for project_node, num_subjects in proj_dict.items():
                project_node.set_label(
                    Text(f'[{num_subjects:>{num_digits}} SUB] {cast(ProjectData, project_node.data).project}'))

            self.root.set_label(Text(f'[{len(self.root.children):>2}] Archive'))

    @on(Tree.NodeExpanded)
    @on(Tree.NodeHighlighted)
    async def update_output_pane(self, event: Tree.NodeExpanded | Tree.NodeHighlighted) -> None:
        self.post_message(XnatTree.ViewChanged(Views.XNAT_INFO))

        self.outputs.clear()

        if event.node is None:
            return

        with Loading(self):
            self.outputs.xnat.update(create_markdown(event.node.data))
            self._process_node(event.node)
            try:
                await self.workers.wait_for_complete()
            except WorkerCancelled as e:
                self.logger.debug(e)

    async def filter_projects(self, value: str) -> None:
        self.root.remove_children()

        for project in sorted(self.session.projects.values(), key=lambda x: x.name.casefold()):  # type: ignore
            if not str(project.name).casefold().startswith(value.casefold()):
                continue
            self.root.add(project.name, project)

        self.root.expand()
        self.root.set_label(Text(f'[{len(self.root.children):>2}] Archive'))
