from typing import TYPE_CHECKING, cast

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, Input

import os

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class LoginWidget(Widget):
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
        self.border_title = "Enter your login credentials"
        self.submit_ready = False

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="cl-login-container"):
                yield Input(
                    value=os.getenv("PROPEL_USER_NAME"),
                    placeholder="Username",
                    id="username",
                )
                yield Input(
                    value=os.getenv("PROPEL_PASSWORD"),
                    placeholder="Password",
                    id="password",
                    password=True,
                )
                yield Button.success("Login", id="login-button")

    @on(Button.Pressed)
    async def on_click(self):
        self.genie.scaffold.login()
        error = self.genie.scaffold.config.detail

        if error:
            response = self.genie.scaffold.config.detail
            self.genie.notify(response, severity="error")
        else:
            os.environ["Token"] = self.genie.scaffold.config.token

            self.genie.scaffold_config = self.genie.scaffold.config
            self.refresh()
            self.genie.pop_screen()
            self.genie.notify("Login Successful")
