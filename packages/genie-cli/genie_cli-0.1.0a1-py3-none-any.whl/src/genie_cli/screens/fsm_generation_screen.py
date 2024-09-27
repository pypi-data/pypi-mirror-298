from typing import TYPE_CHECKING, Optional, cast

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.signal import Signal
from textual.widgets import Footer

from src.genie_cli.runtime_config import RuntimeConfig
from src.genie_cli.widgets.app_header import AppHeader
from src.genie_cli.widgets.chat_options import OptionsModal
from src.genie_cli.widgets.prompt_input import PromptInput

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class HomePromptInput(PromptInput):
    BINDINGS = [Binding("escape", "app.quit", "Exit Genie", key_display="esc")]


class FSMGenerationScreen(Screen[None]):
    CSS = """\
ChatList {
    height: 1fr;
    width: 1fr;
    background: $background 15%;
}
"""

    BINDINGS = [
        Binding(
            "ctrl+j,alt+enter",
            "send_message",
            "Send message",
            priority=True,
            key_display="^j",
        ),
        Binding("o,ctrl+o", "options", "Options", key_display="^o"),
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
        prompt_title = self.genie.query_one(HomePromptInput)
        prompt_title.border_title = "Enter your [u]A[/]gent [u]D[/]escription..."

    def compose(self) -> ComposeResult:
        yield AppHeader(self.config_signal, screen_name="FSM Generation")
        yield HomePromptInput(id="home-prompt")
        yield Footer()

    @on(PromptInput.PromptSubmitted)
    async def create_new_chat(self, event: PromptInput.PromptSubmitted) -> None:
        text = event.text
        await self.genie.launch_scaffolding(
            prompt=text, model=self.genie.runtime_config.selected_model
        )

    async def action_send_message(self) -> None:
        self.notify("Scaffolding started, this might take a while...")
        prompt_input = self.query_one(PromptInput)
        prompt_input.action_submit_prompt()

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
