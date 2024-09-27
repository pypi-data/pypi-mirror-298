from typing import TYPE_CHECKING, cast, Optional
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import ScreenResume
from textual.screen import Screen
from textual.signal import Signal
from textual.widgets import Footer
from zipfile import ZipFile

from src.genie_cli.runtime_config import RuntimeConfig
from src.scaffolding_client.scaffold import ScaffoldConfig

from src.genie_cli.screens.login_screen import LoginScreen

# from src.genie_cli.chats_manager import ChatsManager
from src.genie_cli.widgets.app_header import AppHeader
from src.genie_cli.widgets.welcome import Welcome
from src.genie_cli.widgets.chat_options import OptionsModal
from src.genie_cli.widgets.skill_options import SkillOptionsModal
from src.genie_cli.screens.scaffold_screen import ScaffoldScreen
from src.genie_cli.screens.fsm_generation_screen import FSMGenerationScreen
from src.genie_cli.screens.code_generation_screen import CodeGenerationScreen

from src.genie_cli.states.states import States

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class HomeScreen(Screen[None]):
    BINDINGS = [
        Binding("o,ctrl+o", "options", "Options", key_display="^o"),
        Binding("l", "login", "Login", priority=True, key_display="l"),
        Binding("q", "app.quit", "Quit", key_display="q"),
    ]

    def __init__(
        self,
        config_signal: Signal[RuntimeConfig],
        scaffold_signal: Signal[ScaffoldConfig],
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
        yield AppHeader(self.config_signal, screen_name="Home")
        yield Welcome()
        yield Footer()

    @on(ScreenResume)
    async def reload_screen(self) -> None:
        token = self.genie.scaffold.config.token
        build_id = self.genie.scaffold.config.build_id

        if self.genie.runtime_config.current_state == States.SCAFFOLDING:
            if token and not build_id:
                await self.app.push_screen(
                    ScaffoldScreen(self.config_signal),
                    callback=self.update_config,
                )
            elif token and build_id:
                self.genie.notify(build_id)
                self.app.push_screen(
                    FSMGenerationScreen(self.config_signal),
                    callback=self.update_config,
                )
            else:
                pass
        elif self.genie.runtime_config.current_state == States.SKILL_SELECTION:
            if not self.genie.runtime_config.service_path:
                await self.genie.scaffold.agent_download()
                with ZipFile(
                    self.genie.scaffold.config.build_id + ".zip", "r"
                ) as zip_ref:
                    zip_ref.extractall(self.genie.scaffold.config.build_id)
            await self.app.push_screen(
                SkillOptionsModal(),
                callback=self.update_config,
            )
        elif self.genie.runtime_config.current_state == States.BEHAVIOUR_PLANNING:
            self.app.push_screen(
                CodeGenerationScreen(self.config_signal),
                callback=self.update_config,
            )

    async def action_options(self) -> None:
        await self.app.push_screen(
            OptionsModal(),
            callback=self.update_config,
        )

    async def action_login(self) -> None:
        await self.app.push_screen(
            LoginScreen(self.config_signal),
            callback=self.update_scaffold_config,
        )

    def update_config(self, runtime_config: Optional[RuntimeConfig]) -> None:
        if runtime_config is None:
            return
        app = cast("ServiceEngine", self.app)
        app.runtime_config = runtime_config

    def update_scaffold_config(self, scaffold_config: Optional[ScaffoldConfig]) -> None:
        if scaffold_config is None:
            return
        app = cast("ServiceEngine", self.app)
        app.scaffold_config = scaffold_config
