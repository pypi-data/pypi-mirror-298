from typing import TYPE_CHECKING, cast
from importlib.metadata import version
from rich.markup import escape
from rich.style import Style
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.signal import Signal
from textual.widget import Widget
from textual.widgets import Label, Static

from rich.text import Text
from src.genie_cli.config import ServiceChatModel
from src.genie_cli.models import get_model
from src.genie_cli.runtime_config import RuntimeConfig


if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class AppHeader(Widget):
    COMPONENT_CLASSES = {"app-title", "app-subtitle"}

    def __init__(
        self,
        config_signal: Signal[RuntimeConfig],
        screen_name: str | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.config_signal: Signal[RuntimeConfig] = config_signal
        self.elia = cast("ServiceEngine", self.app)
        self.screen_name = screen_name

    def on_mount(self) -> None:
        def on_config_change(config: RuntimeConfig) -> None:
            self._update_selected_model(config.selected_model)

        self.config_signal.subscribe(self, on_config_change)

    def compose(self) -> ComposeResult:
        title_style = self.get_component_rich_style("app-title")
        subtitle_style = self.get_component_rich_style("app-subtitle")

        with Horizontal():
            with Vertical(id="cl-header-container"):
                yield Label(
                    Text.assemble(
                        ("genie ", title_style + Style(bold=True)),
                        ("///", subtitle_style),
                        (f" {version('genie-cli')}", title_style),
                    )
                )
            if self.screen_name:
                with Vertical(id="cl-screen-container"):
                    yield Static(
                        Text.assemble((self.screen_name, subtitle_style)),
                        id="screen-label",
                    )

            model_name_or_id = (
                self.elia.runtime_config.selected_model.id
                or self.elia.runtime_config.selected_model.name
            )
            model = get_model(model_name_or_id, self.elia.launch_config)
            yield Label(self._get_selected_model_link_text(model), id="model-label")

    def _get_selected_model_link_text(self, model: ServiceChatModel) -> str:
        return f"[@click=screen.options]{escape(model.display_name or model.name)}[/]"

    def _update_selected_model(self, model: ServiceChatModel) -> None:
        print(self.elia.runtime_config)
        model_label = self.query_one("#model-label", Label)
        model_label.update(self._get_selected_model_link_text(model))
