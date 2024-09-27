from typing import TYPE_CHECKING, cast
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Markdown


if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine

TEXT = """
# Welcome to Genie CLI
# Genie is an autonomous service creation tool that helps you build end-to-end services. The CLI tool is designed to help you create services with ease.
# It starts with the propel login process and then iterative steps to create a service. Each step has certain type of LLM agents involved to help you create the service.
# THE APP IS CURRENTLY IN ALPHA STAGE AND MIGHT HAVE BUGS. PLEASE REPORT ANY BUGS TO THE DEVELOPMENT TEAM.
# --------------------
# Press 'l' to login
"""


class Welcome(Widget):
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
        pass

    def compose(self) -> ComposeResult:
        yield Markdown(TEXT)
