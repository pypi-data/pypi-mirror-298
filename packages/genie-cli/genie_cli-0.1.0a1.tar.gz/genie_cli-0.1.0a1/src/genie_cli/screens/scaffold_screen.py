from typing import TYPE_CHECKING, cast, Optional
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import ScreenResume
from textual.screen import Screen
from textual.signal import Signal
from textual.widgets import Footer

from src.genie_cli.runtime_config import RuntimeConfig

# from src.genie_cli.chats_manager import ChatsManager
from src.genie_cli.widgets.app_header import AppHeader
from src.genie_cli.widgets.scaffold_widget import ScaffoldWidget


from src.genie_cli.widgets.chat_options import OptionsModal

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class ScaffoldScreen(Screen[None]):
    BINDINGS = [
        Binding("o,ctrl+o", "options", "Options", key_display="^o"),
        Binding("l", "login", "Login", priority=True, key_display="l"),
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
        self.genie = cast("ServiceEngine", self.app)

    def on_mount(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        yield AppHeader(self.config_signal, screen_name="Scaffold")
        yield ScaffoldWidget()
        yield Footer()

    @on(ScreenResume)
    async def reload_screen(self) -> None:
        # if self.app.runtime_config.current_state == "skill_selection":
        #     await self.app.push_screen(SkillInput(self.elia.runtime_config_signal))
        pass

    async def action_options(self) -> None:
        await self.app.push_screen(
            OptionsModal(),
            callback=self.update_config,
        )

    def update_config(self, runtime_config: Optional[RuntimeConfig]) -> None:
        if runtime_config is None:
            return
        app = cast("ServiceEngine", self.app)
        app.runtime_config = runtime_config
