from __future__ import annotations

import datetime
import os
import random
import subprocess
import threading
import time
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import SecretStr
from textual.app import App
from textual.binding import Binding
from textual.signal import Signal

from src.genie_cli.config import LaunchConfig, ServiceChatModel, launch_config
from src.genie_cli.models import ChatData, ChatMessage
from src.genie_cli.prompts.behaviour_prompts import (
    BEHAVIOUR_EXAMPLE_3,
    BEHAVIOUR_PLANNER_EXAMPLE,
    BEHAVIOUR_PLANNER_PROMPT,
    BEHAVIOUR_PLANNER_USER_MESSAGE,
    BEHAVIOUR_USER_MESSAGE,
)
from src.genie_cli.prompts.rounds_prompts import (
    ROUNDS_SYSTEM_PROMPT,
    ROUNDS_EXAMPLE_1,
    ROUNDS_SYSTEM_PROMPT,
    ROUND_PLANNER_EXAMPLE,
    ROUND_PLANNER_USER_MESSAGE,
    ROUND_TASK_DESCRIPTION,
)
from src.genie_cli.prompts.round_code_examples import (
    ROUND_EXAMPLE_1_CODE,
    BASE_SYNC_DATA_CLASS,
)
from src.genie_cli.runtime_config import RuntimeConfig
from src.genie_cli.screens.chat_screen import ChatScreen, ScaffoldChatScreen
from src.genie_cli.screens.home_screen import HomeScreen
from src.scaffolding_client.scaffold import Scaffold, ScaffoldConfig

if TYPE_CHECKING:
    from litellm.types.completion import (
        ChatCompletionAssistantMessageParam,
        ChatCompletionSystemMessageParam,
        ChatCompletionUserMessageParam,
    )


def open_file_in_ide(file_path):
    subprocess.run(
        ["zed", file_path]
    )  # TODO: Change this to open the file in ide from env variable


def write_live_text(file_path, text_to_add, interval=5):
    with open(file_path, "w") as f:
        f.write("")

    for char in text_to_add:
        with open(file_path, "a") as f:
            f.write(char)
            time.sleep(0.01)
    time.sleep(interval)


def writer_service(file_path, content):
    # Open the file in VSCode
    open_file_in_ide(file_path)

    # Start a separate thread to write live text to the file
    writer_thread = threading.Thread(target=write_live_text, args=(file_path, content))
    writer_thread.start()
    writer_thread.join()  # Wait for the thread to complete


def code_loader(skill_path):
    """Extract behaviors.py file from skill path."""
    behaviors_path = skill_path
    if os.path.exists(behaviors_path):
        with open(behaviors_path) as f:
            behaviors_code = f.read()
        return behaviors_code
    else:
        raise FileNotFoundError(f"The file {behaviors_path} does not exist.")


class ServiceEngine(App[None]):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = Path(__file__).parent.parent / "frontend" / "css" / "service_engine.scss"
    BINDINGS = [
        Binding("q", "app.quit", "Quit", show=False),
        Binding("f1,?", "help", "Help"),
    ]

    def __init__(
        self,
        config: LaunchConfig,
        scaffold_config: ScaffoldConfig,
        startup_prompt: str = "",
    ):
        super().__init__()
        self.launch_config = config
        launch_config.set(config)
        self._runtime_config = RuntimeConfig(
            selected_model=config.default_model_object,
            system_prompt=config.system_prompt,
        )
        self.runtime_config_signal = Signal[RuntimeConfig](
            self, "runtime-config-updated"
        )
        self._scaffold_config: ScaffoldConfig = scaffold_config
        self.scaffold_config_signal = Signal[ScaffoldConfig](
            self, "scaffold-config-updated"
        )

        self.scaffold = Scaffold(self._scaffold_config)
        """Widgets can subscribe to this signal to be notified of
        when the user has changed configuration at runtime (e.g. using the UI)."""

        self.startup_prompt = startup_prompt
        """Genie can be launched with a prompt on startup via a command line option.

        This is a convenience which will immediately load the chat interface and
        put users into the chat window, rather than going to the home screen.
        """

    @property
    def runtime_config(self) -> RuntimeConfig:
        return self._runtime_config

    @property
    def scaffold_config(self) -> ScaffoldConfig:
        return self._scaffold_config

    @scaffold_config.setter
    def scaffold_config(self, new_runtime_config: ScaffoldConfig) -> None:
        self._scaffold_config = new_runtime_config
        self.scaffold = Scaffold(self._scaffold_config)
        self.scaffold_config_signal.publish(self.scaffold_config)

    @runtime_config.setter
    def runtime_config(self, new_runtime_config: RuntimeConfig) -> None:
        self._runtime_config = new_runtime_config
        self.runtime_config_signal.publish(self.runtime_config)

    async def on_mount(self) -> None:
        self.push_screen(
            HomeScreen(self.runtime_config_signal, self.scaffold_config_signal)
        )

    async def launch_scaffolding(self, prompt: str, model: ServiceChatModel) -> None:
        current_time = datetime.datetime.now(datetime.UTC)
        system_message: ChatCompletionSystemMessageParam = {
            "content": "Generate FSM for the given description.",
            "role": "system",
        }
        user_message: ChatCompletionUserMessageParam = {
            "content": prompt,
            "role": "user",
        }

        chat = ChatData(
            id=random.randint(0, 1000000),
            title="Scaffolding Chat",
            create_timestamp=None,
            model=model,
            messages=[
                ChatMessage(
                    message=system_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message,
                    timestamp=current_time,
                    model=model,
                ),
            ],
        )

        await self.push_screen(ScaffoldChatScreen(chat))

    async def launch_behaviour_planner_chat(
        self, prompt: str, model: ServiceChatModel
    ) -> None:
        current_time = datetime.datetime.now(datetime.UTC)

        ##################################################### LOADING COMPONENT FILES #####################################################
        # Crearing file paths
        behavior_file_abs_path = os.path.join(
            self.runtime_config.skill_path, "behaviours.py"
        )

        # loading files
        behaviour_code_content = code_loader(behavior_file_abs_path)

        ##################################################### GENERATING COMPONENTS SYSTEM PROMPTS #####################################################

        # Loading behaviour system prompt
        # behaviour_system_prompt = system_prompt_loader(prompt, behaviour_code_content)

        system_message: ChatCompletionSystemMessageParam = {
            "content": BEHAVIOUR_PLANNER_PROMPT,
            "role": "system",
        }
        user_message: ChatCompletionUserMessageParam = {
            "content": BEHAVIOUR_PLANNER_USER_MESSAGE.format(
                skill_description=prompt,
                code_content=behaviour_code_content,
                planner_example=BEHAVIOUR_PLANNER_EXAMPLE,
            ),
            "role": "user",
        }

        chat = ChatData(
            id=random.randint(0, 1000000),
            title="Behaviour Planner Chat",
            create_timestamp=None,
            model=model,
            messages=[
                ChatMessage(
                    message=system_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message,
                    timestamp=current_time,
                    model=model,
                ),
            ],
        )

        await self.push_screen(
            ChatScreen(config_signal=self.runtime_config_signal, chat_data=chat)
        )

    async def launch_behaviour_generation_chat(
        self, prompt: str, model: ServiceChatModel
    ) -> None:
        current_time = datetime.datetime.now(datetime.UTC)

        ##################################################### LOADING COMPONENT FILES #####################################################
        # Crearing file paths
        behavior_file_abs_path = os.path.join(
            self.runtime_config.skill_path, "behaviours.py"
        )
        round_file_abs_path = os.path.join(self.runtime_config.skill_path, "rounds.py")

        # loading files
        behaviour_code_content = code_loader(behavior_file_abs_path)
        try:
            round_code_content = code_loader(round_file_abs_path)
        except Exception:
            self.runtime_config = self.runtime_config.model_copy(
                update={"rounds_available": False}
            )

        ##################################################### GENERATING COMPONENTS SYSTEM PROMPTS #####################################################

        system_message: ChatCompletionSystemMessageParam = {
            "content": self.runtime_config.behaviour_plan,
            "role": "system",
        }
        user_message: ChatCompletionUserMessageParam = {
            "content": BEHAVIOUR_EXAMPLE_3.replace("{", "{{").replace("}", "}}"),
            "role": "user",
        }
        ai_message: ChatCompletionAssistantMessageParam = {
            "content": "Thank you for providing the context and an example code file. I'm ready to assist you with writing the code based on your skill requirements. Please go ahead and provide me your skill requirements and code that you want to complete.",
            "role": "assistant",
        }
        user_message_2: ChatCompletionUserMessageParam = {
            "content": BEHAVIOUR_USER_MESSAGE.format(
                code_content=behaviour_code_content, user_requirement=prompt
            ),
            "role": "user",
        }

        chat = ChatData(
            id=random.randint(0, 1000000),
            title="Behaviour Generation Chat",
            create_timestamp=None,
            model=model,
            messages=[
                ChatMessage(
                    message=system_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=ai_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message_2,
                    timestamp=current_time,
                    model=model,
                ),
            ],
        )

        await self.push_screen(
            ChatScreen(config_signal=self.runtime_config_signal, chat_data=chat)
        )

    async def launch_round_planner_chat(
        self, prompt: str, model: ServiceChatModel
    ) -> None:
        current_time = datetime.datetime.now(datetime.UTC)

        ##################################################### LOADING COMPONENT FILES #####################################################
        # Crearing file paths
        round_file_abs_path = os.path.join(self.runtime_config.skill_path, "rounds.py")

        # loading files
        round_code_content = code_loader(round_file_abs_path)

        ##################################################### GENERATING COMPONENTS SYSTEM PROMPTS #####################################################

        # Loading behaviour system prompt
        # behaviour_system_prompt = system_prompt_loader(prompt, behaviour_code_content)

        system_message: ChatCompletionSystemMessageParam = {
            "content": ROUNDS_SYSTEM_PROMPT,
            "role": "system",
        }
        user_message: ChatCompletionUserMessageParam = {
            "content": ROUND_PLANNER_USER_MESSAGE.format(
                skill_description=prompt,
                planner_example=ROUND_PLANNER_EXAMPLE,
                code_content=round_code_content,
            ),
            "role": "user",
        }

        chat = ChatData(
            id=random.randint(0, 1000000),
            title="Round Planner Chat",
            create_timestamp=None,
            model=model,
            messages=[
                ChatMessage(
                    message=system_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message,
                    timestamp=current_time,
                    model=model,
                ),
            ],
        )

        await self.push_screen(
            ChatScreen(config_signal=self.runtime_config_signal, chat_data=chat)
        )

    async def launch_round_code_generation(
        self, prompt: str, model: ServiceChatModel
    ) -> None:
        current_time = datetime.datetime.now(datetime.UTC)

        ##################################################### LOADING COMPONENT FILES #####################################################
        # Crearing file paths
        round_file_abs_path = os.path.join(self.runtime_config.skill_path, "rounds.py")
        behavior_file_abs_path = os.path.join(
            self.runtime_config.skill_path, "behaviours.py"
        )

        # loading files
        round_code_content = code_loader(round_file_abs_path)
        behaviour_code_content = code_loader(behavior_file_abs_path)

        ##################################################### GENERATING COMPONENTS SYSTEM PROMPTS #####################################################

        system_message: ChatCompletionSystemMessageParam = {
            "content": self.runtime_config.rounds_plan,
            "role": "system",
        }
        user_message: ChatCompletionUserMessageParam = {
            "content": ROUNDS_EXAMPLE_1.format(
                round_example_1=ROUND_EXAMPLE_1_CODE.replace("{", "{{").replace(
                    "}", "}}"
                )
            ),
            "role": "user",
        }
        ai_message: ChatCompletionAssistantMessageParam = {
            "content": "hank you for providing the context and an example code file. I'm ready to assist you with writing the code based on your requirements. Please go ahead and provide me with the next example to improve my understanding.",
            "role": "assistant",
        }
        user_message_2: ChatCompletionUserMessageParam = {
            "content": ROUND_TASK_DESCRIPTION.format(
                code_content=round_code_content,
                base_sync_data_class=BASE_SYNC_DATA_CLASS,
                behavior_code=behaviour_code_content,
            ),
            "role": "user",
        }

        chat = ChatData(
            id=None,
            title=None,
            create_timestamp=None,
            model=model,
            messages=[
                ChatMessage(
                    message=system_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=ai_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message_2,
                    timestamp=current_time,
                    model=model,
                ),
            ],
        )

        await self.push_screen(
            ChatScreen(config_signal=self.runtime_config_signal, chat_data=chat)
        )


if __name__ == "__main__":
    username = os.getenv("PROPEL_USER_NAME", "admin")
    password = os.getenv("PROPEL_PASSWORD", "admin")
    openai_api_key = os.getenv("OPENAI_API_KEY", "admin")
    author = os.getenv("AUTHOR", "admin")
    app = ServiceEngine(
        LaunchConfig(),
        ScaffoldConfig(
            username=username,
            password=SecretStr(password),
            openai_api_key=SecretStr(openai_api_key),
            author=author,
        ),
    )
    app.run()
