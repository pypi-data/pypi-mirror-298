import enum
from dataclasses import dataclass
from typing import Any

from textual import work
from textual.app import ComposeResult, App
from textual.containers import Grid, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Input, Switch, Select, Rule


class QuitScreen(ModalScreen):
    """Screen with a dialog to quit."""
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    QuitScreen {
        align: center middle;
    }
    
    QuitScreen Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 40;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }
    
    QuitScreen Label {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }    
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Label('Are you sure you want to quit?', id='question'),
            Button('Quit', variant='error', id='quit'),
            Button('Cancel', variant='primary', id='cancel'),
            id='quit_dialog',
        )

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'quit':
            self.app.exit()
        else:
            self.app.pop_screen()


class PrearchiveActionResult(enum.IntEnum):
    ARCHIVE = enum.auto()
    REBUILD = enum.auto()
    DELETE = enum.auto()
    MOVE = enum.auto()


class PrearchiveActionsScreen(ModalScreen[PrearchiveActionResult]):
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    PrearchiveActionsScreen {
        align: center middle;
        width: auto;
        height: auto;
    }

    PrearchiveActionsScreen Vertical {
        height: auto;
        width: auto;
    }

    PrearchiveActionsScreen Horizontal {
        width: auto;
        height: auto;
    }

    PrearchiveActionsScreen Horizontal Button {
        margin: 2;
        width: 10;
    }
    """

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button('Archive', id='archive')
            yield Button('Rebuild', id='rebuild')
            yield Button('Move', id='move')
            yield Button('Delete', id='delete')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case 'archive':
                self.dismiss(PrearchiveActionResult.ARCHIVE)
            case 'rebuild':
                self.dismiss(PrearchiveActionResult.REBUILD)
            case 'delete':
                self.dismiss(PrearchiveActionResult.DELETE)
            case 'move':
                self.dismiss(PrearchiveActionResult.MOVE)
            case _:
                raise RuntimeError(f'Unknown button pressed "{event.button.id}"')

    def action_pop_screen(self) -> None:
        self.app.pop_screen()


class ConfirmationResult(enum.IntEnum):
    YES = enum.auto()
    NO = enum.auto()


class ConfirmationScreen(ModalScreen[ConfirmationResult]):
    """Screen with a dialog to confirm or cancel an action."""
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    ConfirmationScreen {
        align: center middle;
    }

    ConfirmationScreen Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 40;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }

    ConfirmationScreen Label {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }    
    """

    def __init__(self, action_text: str) -> None:
        super().__init__()
        self.action_text = action_text

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.action_text, id='question'),
            Button('Yes', variant='primary', id='yes'),
            Button('No', variant='error', id='no'),
            id='confirmation_dialog',
        )

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case 'yes':
                self.dismiss(ConfirmationResult.YES)
            case 'no':
                self.dismiss(ConfirmationResult.NO)
            case _:
                raise RuntimeError(f'Unknown button pressed "{event.button.id}"')


class Overwrite(enum.StrEnum):
    NONE = 'none'
    APPEND = 'append'
    DELETE = 'delete'


@dataclass
class ArchiveResult:
    project: str
    subject: str
    experiment: str
    overwrite: Overwrite = Overwrite.NONE
    quarantine: bool = False
    trigger_pipelines: bool = False


def enum_value_asdict_factory(data: list[tuple[str, Any]]) -> dict[Any, Any]:
    def convert_value(obj: Any) -> Any:
        if isinstance(obj, enum.Enum):
            return obj.value
        return obj

    return dict((k, convert_value(v)) for k, v in data)


class ArchiveScreen(ModalScreen[ArchiveResult | None]):
    """Screen with a dialog to confirm or cancel an action."""
    BINDINGS = [
        ('escape', 'pop_screen')
    ]
    CSS_PATH = 'screen.tcss'

    DEFAULT_CSS = """
    ArchiveScreen {
        align: center middle;
    }

    ArchiveScreen  Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 100;
        height: 100%;
        border: thick $background 80%;
        background: $surface;
    }

    ArchiveScreen Input {
        column-span: 2;
        height: 3;
        width: 1fr;
        content-align: center middle;
    }
    """

    def __init__(self, project: str | None, subject: str | None, experiment: str | None) -> None:
        super().__init__()
        self.project = project
        self.subject = subject
        self.experiment = experiment

    def compose(self) -> ComposeResult:
        with Grid(id='archive_dialog'):
            yield Label('Project:')
            yield Input(value=self.project, placeholder='Project', id='project_input')
            yield Label('Subject:')
            yield Input(value=self.subject, placeholder='Subject', id='subject_input')
            yield Label('Experiment:')
            yield Input(value=self.experiment, placeholder='Experiment', id='experiment_input')
            yield Label('Overwrite:', id='overwrite')
            yield Select([('None', Overwrite.NONE), ('Append', Overwrite.APPEND), ('Delete', Overwrite.DELETE)],
                         allow_blank=False, value=Overwrite.NONE, id='overwrite_select')
            yield Label('Quarantine:')
            yield Switch(id='switch_quarantine')
            yield Label('Trigger pipelines:')
            yield Switch(id='switch_trigger_pipelines')
            yield Rule(line_style='double')
            yield Label('Proceed with archive action?', id='question')
            with Horizontal():
                yield Button('Yes', variant='primary', id='yes')
                yield Button('No', variant='error', id='no')

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        result = ArchiveResult(project=self.query_exactly_one('#project_input', Input).value,
                               subject=self.query_exactly_one('#subject_input', Input).value,
                               experiment=self.query_exactly_one('#experiment_input', Input).value,
                               overwrite=self.query_exactly_one('#overwrite_select', Select).value,  # type: ignore
                               quarantine=self.query_exactly_one('#switch_quarantine', Switch).value,
                               trigger_pipelines=self.query_exactly_one('#switch_trigger_pipelines', Switch).value)

        match event.button.id:
            case 'yes':
                self.dismiss(result)
            case 'no':
                self.dismiss(None)
            case _:
                raise RuntimeError(f'Unknown button pressed "{event.button.id}"')


class ScreenApp(App):
    @work
    async def on_mount(self) -> None:
        print(await self.push_screen_wait(ArchiveScreen(project='project', subject='subject', experiment='experiment')))

        self.app.exit()


if __name__ == "__main__":
    app = ScreenApp()
    app.run()
