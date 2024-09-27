from typing import TYPE_CHECKING, cast

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, Input

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class ScaffoldWidget(Widget):
    COMPONENT_CLASSES = {"app-title", "app-subtitle"}

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.genie = cast("ServiceEngine", self.app)

    def on_mount(self) -> None:
        self.border_title = "Enter your agent details"
        self.submit_ready = False
        self.genie.notify("The agent building process will take a few minutes(2-3 minutes)", timeout=15, severity="info")

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="cl-login-container"):
                yield Input(placeholder="Agent Name", id="agent-name")
                yield Button.success("Scaffold", id="scaffold-button")

    @on(Button.Pressed)
    async def on_click(self):
        agent_name = self.query_one("#agent-name", Input).value

        self.genie.notify(f"Initiating build for {agent_name}")

        message = self.genie.scaffold.init_build(name=agent_name)

        if message == "Project found in the directory.":
            self.genie.notify("Please use a different agent name")
        else:
            self.genie.notify("Build completed successfully")
            self.genie.scaffold_config = self.genie.scaffold.config
            self.genie.pop_screen()
