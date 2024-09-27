from __future__ import annotations
from typing import TYPE_CHECKING, cast
import os


from rich.markup import escape
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Footer, RadioSet, RadioButton, TextArea

from src.genie_cli.constants import IGNORE_SKILLS
from src.genie_cli.runtime_config import RuntimeConfig
from src.genie_cli.states.states import States

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class ModelRadioButton(RadioButton):
    def __init__(
        self,
        label: str | Text = "",
        value: bool = False,
        button_first: bool = True,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            label,
            value,
            button_first,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )


class SkillOptionsModal(ModalScreen[RuntimeConfig]):
    BINDINGS = [
        Binding("q", "app.quit", "Quit", show=False),
        Binding("s", "app.pop_screen", "Select Skill", key_display="s"),
        Binding("escape", "app.pop_screen", "Close options", key_display="esc"),
    ]

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.genie = cast("ServiceEngine", self.app)
        self.runtime_config = self.genie.runtime_config

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="skill-scrollable") as vs:
            vs.border_title = "Skill Options"
            vs.can_focus = False
            available_skills = []

            # Add available skills to the list
            BASE_PATH = self.genie.scaffold.config.build_id
            PACKAGES_PATH = os.path.join(BASE_PATH, "packages/valory/skills")
            for folder in os.listdir(PACKAGES_PATH):
                if (
                    os.path.isdir(os.path.join(PACKAGES_PATH, folder))
                    and folder not in IGNORE_SKILLS
                ):
                    if os.path.exists(os.path.join(PACKAGES_PATH, folder, "rounds.py")):
                        available_skills.append(folder)

            with RadioSet(id="available-skills") as models_rs:
                models_rs.border_title = "Available Skills"
                for skill in available_skills:
                    label = f"[dim]{escape(skill)}"

                    yield ModelRadioButton(
                        value=False,
                        label=label,
                    )

            selected_kill_ta = TextArea(available_skills[0], id="selected-skill-ta")
            selected_kill_ta.border_title = "Selected skill"
            yield selected_kill_ta
            # TODO - yield and dock a label to the bottom explaining
            #  that the changes made here only apply to the current session
            #  We can probably do better when it comes to system prompts.
            #  Perhaps we could store saved prompts in the database.
        yield Footer()

    def on_mount(self) -> None:
        pass

    @on(RadioSet.Changed)
    @on(TextArea.Changed)
    def update_state(self, event: TextArea.Changed | RadioSet.Changed) -> None:
        selected_skill_ta = self.query_one("#selected-skill-ta", TextArea)
        selected_model_rs = self.query_one("#available-skills", RadioSet)
        if selected_model_rs.pressed_button is None:
            selected_model_rs._selected = 0
            assert selected_model_rs.pressed_button is not None
        else:
            selected_skill_ta.text = str(selected_model_rs.pressed_button.label)

        model_button = cast(ModelRadioButton, selected_model_rs.pressed_button)
        skill = str(model_button.label)
        BASE_PATH = self.genie.scaffold.config.build_id
        PACKAGES_PATH = os.path.join(BASE_PATH, "packages/valory/skills")
        self.genie.runtime_config = self.genie.runtime_config.model_copy(
            update={
                "service_path": BASE_PATH,
                "skill_path": os.path.join(PACKAGES_PATH, skill),
                "current_state": States.BEHAVIOUR_PLANNING
            }
        )
        self.refresh()

    def apply_overridden_subtitles(
        self, system_prompt_ta: TextArea, selected_model_rs: RadioSet
    ) -> None:
        if (
            self.genie.launch_config.default_model
            != self.genie.runtime_config.selected_model.id
            and self.genie.launch_config.default_model
            != self.genie.runtime_config.selected_model.name
        ):
            selected_model_rs.border_subtitle = "overrides config"
        else:
            selected_model_rs.border_subtitle = ""

        if system_prompt_ta.text != self.genie.launch_config.system_prompt:
            system_prompt_ta.border_subtitle = "overrides config"
        else:
            system_prompt_ta.border_subtitle = ""
