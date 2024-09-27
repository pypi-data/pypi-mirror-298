import logging

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import ScrollableContainer, Horizontal, Vertical
from textual.widgets import Header, Footer, Label, Input, RichLog, TabbedContent, TabPane

from xnat_browser.app_base import XnatBase
from xnat_browser.image_viewer import ImageViewer
from xnat_browser.xnat_archive_tree import XnatArchiveTree
from xnat_browser.xnat_prearchive_tree import XnatPrearchiveTree
from xnat_browser.xnat_tree import XnatTree, Outputs, Views


class XnatBrowser(XnatBase):
    CSS_PATH = 'browser.tcss'
    BINDINGS = [
        Binding('u', 'update_projects', 'Update projects', show=False),
        Binding('f5', 'refresh', 'Refresh'),
        Binding('ctrl+f', 'filter_project', 'Filter Project'),
    ]

    def __init__(self, server: str, username: str | None = None, password: str | None = None,
                 log_level: int = logging.INFO) -> None:
        super().__init__(server, username, password, log_level)

    def compose(self) -> ComposeResult:
        logger = self._setup_logging()
        outputs = Outputs(
            xnat=Label(id='xnat_info', expand=True),
            dicom=Label(id='dicom_info', expand=True),
            image=ImageViewer(id='image_info'),
        )
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical():
                widget = Input(placeholder='Project', id='project_search', classes='remove')
                widget.border_title = 'Filter projects'
                yield widget
                with TabbedContent(id='source_tabbed_content') as tabbed_content:
                    tabbed_content.border_title = 'Source'
                    with TabPane('Archive'):
                        archive = XnatArchiveTree(outputs, self.logger, id='xnat_tree')
                        archive.border_title = 'Archive'
                        archive.focus()
                        yield archive
                    with TabPane('Pre-Archive'):
                        prearchive = XnatPrearchiveTree(outputs, self.logger, id='xnat_tree_pre_archive')
                        prearchive.border_title = 'Pre-Archive'
                        yield prearchive
            with TabbedContent(id='info_tabbed_content', initial='xnat_info_tab') as tabbed_content:
                tabbed_content.border_title = 'Info'
                with TabPane('XNAT', id='xnat_info_tab'):
                    with ScrollableContainer(id='xnat_info_container'):
                        yield outputs.xnat
                with TabPane('DICOM', id='dicom_info_tab'):
                    with ScrollableContainer(id='dicom_info_container'):
                        yield outputs.dicom
                with TabPane('Image', id='image_tab'):
                    with ScrollableContainer(id='image_container'):
                        yield outputs.image
        yield logger
        yield Footer()

    def on_mount(self) -> None:
        for tree in self.query(XnatTree):  # pylint: disable=not-an-iterable
            tree.set_session(self.session)
        self.query_one('#rich_log', RichLog).border_title = 'Log'
        self.logger.debug('Welcome')

    async def on_input_changed(self, message: Input.Changed) -> None:
        for xnat_tree in self.query(XnatTree):  # pylint: disable=not-an-iterable
            await xnat_tree.filter_projects(str(message.value))

    def action_filter_project(self) -> None:
        widget = self.query_one('#project_search', Input)
        widget.focus()
        widget.toggle_class('remove')

    def action_update_projects(self) -> None:
        active_pane = self.query_one('#source_tabbed_content', TabbedContent).active_pane
        if active_pane is None:
            return
        # noinspection PyArgumentList
        active_pane.query_one(XnatTree).action_update_projects()

    async def action_refresh(self) -> None:
        active_pane = self.query_one('#source_tabbed_content', TabbedContent).active_pane
        if active_pane is None:
            return
        # noinspection PyArgumentList
        await active_pane.query_one(XnatTree).action_refresh()

    @on(TabbedContent.TabActivated)
    async def tab_changed(self, event: TabbedContent.TabActivated) -> None:
        if event.tabbed_content.active in ('dicom_info_tab', 'image_tab'):
            # If any of the DICOM tabs is selected, get the active source (archive or pre-archive) and
            # call the action_dicom method to load the currently selected scan or do nothing if no scan is selected,
            # i.e. an experiment, subject or project is selected.
            active_pane = self.query_one('#source_tabbed_content', TabbedContent).active_pane
            if active_pane is None:
                return
            # noinspection PyArgumentList
            active_pane.query_one(XnatTree).dicom_info()

    @on(XnatTree.ViewChanged)
    async def view_changed(self, event: XnatTree.ViewChanged) -> None:
        tab = self.query_one('#info_tabbed_content', TabbedContent)
        match event.view:
            case Views.XNAT_INFO:
                tab.active = 'xnat_info_tab'
            case Views.DICOM_INFO:
                tab.active = 'dicom_info_tab'
            case Views.DICOM_IMAGE:
                tab.active = 'image_tab'
