from datetime import timedelta, datetime

import humanize
from rich.console import RenderableType
from rich.markdown import Markdown
from xnat.core import XNATBaseObject
from xnat.mixin import ProjectData, ImageScanData, SubjectData, ImageSessionData
from xnat.prearchive import PrearchiveSession, PrearchiveScan


# noinspection PyTypeChecker
def create_markdown(data: XNATBaseObject) -> RenderableType:
    md: RenderableType = Markdown('No information.')
    match data:
        case PrearchiveScan():
            md = _prearchive_scan(data)
        case PrearchiveSession():
            md = _prearchive_session(data)
        case ProjectData():
            md = _project(data)
        case SubjectData():
            md = _subjectdata(data)
        case ImageSessionData():
            md = _image_session(data)
        case ImageScanData():
            md = _scandata(data)

    return md


def _prearchive_scan(data: PrearchiveScan) -> RenderableType:
    markdown = [
        '# Pre-archive scan info.',
        '|Key|Value|',
        '|---|---|',
        f'|ID|{data.id}|',
        f'|Series Description|"{data.series_description}"|',
        f'|Number of files|{len(data.files)}|',
    ]

    return Markdown('\n'.join(markdown))


def _prearchive_session(data: PrearchiveSession) -> RenderableType:
    markdown = [
        '# Pre-archive session info.',
        '|Key|Value|',
        '|---|---|',
        f'|Label|{data.label}|'
    ]

    if data.uploaded:
        markdown.append(f'|Uploaded|{data.uploaded:%Y-%m-%d %H:%M:%S}, {humanize.naturaltime(data.uploaded)}|')
    if data.lastmod:
        markdown.append(f'|Last modified|{data.lastmod:%Y-%m-%d %H:%M:%S}, '
                        f'{humanize.naturaltime(data.lastmod)}|')
    if data.scan_date and data.scan_time:
        scan_date = datetime.combine(data.scan_date, data.scan_time)
        markdown.append(f'|Scan date|{scan_date:%Y-%m-%d %H:%M:%S}, '
                        f'{humanize.naturaltime(scan_date)}|')

    markdown.append(f'|Status|"{data.status}"|')

    return Markdown('\n'.join(markdown))


def _project(data: ProjectData) -> RenderableType:
    markdown = [
        '# Project info.',
        '_General_\n',
        '|||',
        '|---|---|',
    ]

    if data.description:  # type: ignore
        markdown.append(f'|Description|"{data.description}"|')  # type: ignore

    markdown.append(f'|Name|{data.name}|')  # type: ignore

    markdown.append(f'|ID|{data.id}|')
    markdown.append(f'|Secondary ID|{data.secondary_id}|')  # type: ignore

    if data.keywords:  # type: ignore
        keywords = [f"'{x}'" for x in data.keywords.split()]  # type: ignore
        markdown.append(f'|Keywords|{", ".join(keywords)}|')

    try:
        markdown.extend(['\n_Primary Investigator_\n', '|||', '|---|---|', ])
        markdown.append(f'|First name|{data.pi.firstname}|')  # type: ignore
        markdown.append(f'|Last name|{data.pi.lastname}|')  # type: ignore
        markdown.append(f'|E-mail|{data.pi.email}|')  # type: ignore
        markdown.append(f'|Institution|{data.pi.institution}|')  # type: ignore
    except TypeError:
        pass

    try:
        markdown.extend(['\n_Users_\n', '|Name|Role|', '|---|---|', ])
        for _, user in sorted(data.users.data.items(), key=lambda x: x[1].access_level, reverse=True):
            markdown.append(f'|{user.first_name} {user.last_name}|{user.access_level}|')
    except TypeError:
        pass

    return Markdown('\n'.join(markdown))


def _subjectdata(data: SubjectData) -> RenderableType:
    markdown = [
        '# Subject info.',
        '|||',
        '|---|---|',
        f'|Group|{data.group}|',  # type: ignore
        f'|Label|{data.label}|',
        f'|Project|{data.project}|',  # type: ignore
        f'|ID|{data.id}|'
    ]

    return Markdown('\n'.join(markdown))


def _image_session(data: ImageSessionData) -> RenderableType:
    markdown = [
        '# Session info.',
        '|||',
        '|---|---|',
        f'|Acquisition site|{data.acquisition_site}|',  # type: ignore
        f'|Modality|{data.modality}|',  # type: ignore
        f'|Project|{data.project}|',  # type: ignore
    ]
    try:
        markdown.append(f'|Scan date|{data.date:%Y-%m-%d}|')  # type: ignore
        markdown.append(f'|Birth date|{data.dcm_patient_birth_date:%Y-%m-%d}|')  # type: ignore
        age: timedelta = data.date - data.dcm_patient_birth_date  # type: ignore
        markdown.append(f'|Age|{humanize.naturaldelta(age)}|')
    except TypeError:
        markdown.append('- Age: Unknown')

    return Markdown('\n'.join(markdown))


def _scandata(data: ImageScanData) -> RenderableType:
    markdown = ['# Scan info.']

    markdown.extend(['|||', '|---|---|'])
    for key, value in sorted(data.data.items()):
        markdown.append(f'|{key}|{value}|')

    markdown.append(f'|Number of files|{len(data.files)}|')
    return Markdown('\n'.join(markdown))
