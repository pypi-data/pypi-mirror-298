from typing import TYPE_CHECKING, cast
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import ScreenResume
from textual.screen import Screen
from textual.signal import Signal
from textual.widgets import Footer

from src.genie_cli.runtime_config import RuntimeConfig
from src.genie_cli.widgets.app_header import AppHeader
from src.genie_cli.widgets.login_widget import LoginWidget

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class LoginScreen(Screen[None]):
    BINDINGS = [
        Binding("q", "app.quit", "Quit", key_display="q"),
    ]

    def __init__(
        self,
        config_signal: Signal[RuntimeConfig],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.config_signal = config_signal
        self.elia = cast("ServiceEngine", self.app)

    def on_mount(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        yield AppHeader(self.config_signal, screen_name="Login")
        yield LoginWidget()
        yield Footer()

    @on(ScreenResume)
    async def reload_screen(self) -> None:
        pass
