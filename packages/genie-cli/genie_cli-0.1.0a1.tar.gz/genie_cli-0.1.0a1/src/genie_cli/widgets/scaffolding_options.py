from __future__ import annotations

from typing import TYPE_CHECKING, cast

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, TextArea

from src.genie_cli.runtime_config import RuntimeConfig

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class ScaffoldingModal(ModalScreen[RuntimeConfig]):
    BINDINGS = [
        Binding("q", "app.quit", "Quit", show=False),
        Binding("escape", "app.pop_screen", "Close Response", key_display="esc"),
    ]

    def __init__(
        self,
        response: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.genie = cast("ServiceEngine", self.app)
        self.runtime_config = self.genie.runtime_config
        self.response = response

    def compose(self) -> ComposeResult:
        with Vertical(id="form-scrollable") as vs:
            vs.border_title = "Scaffolding Response"
            vs.can_focus = False
            yield TextArea(self.response, read_only=True)
        yield Footer()
