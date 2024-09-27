from logging import raiseExceptions
from typing import TYPE_CHECKING, cast

from textual import on, log
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer
from textual.signal import Signal

# from src.chats_manager import ChatsManager
from src.genie_cli.widgets.agent_is_typing import AgentIsTyping
from src.genie_cli.runtime_config import RuntimeConfig

from src.genie_cli.widgets.chat import Chat
from src.genie_cli.widgets.scaffold_chat import ScaffoldChat
from src.genie_cli.models import ChatData
from src.genie_cli.states.states import States

if TYPE_CHECKING:
    from src.genie_cli.app import ServiceEngine


class ChatScreen(Screen[None]):
    AUTO_FOCUS = "ChatPromptInput"
    BINDINGS = [
        Binding(
            key="escape",
            action="app.focus('prompt')",
            description="Focus prompt",
            key_display="esc",
        ),
        Binding("ctrl+n", "next_step", "Next Step", key_display="^n"),
    ]

    def __init__(
        self,
        config_signal: Signal[RuntimeConfig],
        chat_data: ChatData,
    ):
        super().__init__()
        self.chat_data = chat_data
        self.config_signal = config_signal
        self.genie = cast("ServiceEngine", self.app)
        # self.chats_manager = ChatsManager()

    def compose(self) -> ComposeResult:
        yield Chat(self.chat_data)
        yield Footer()

    @on(Chat.AgentResponseStarted)
    def start_awaiting_response(self) -> None:
        """Prevent sending messages because the agent is typing."""
        self.query_one(AgentIsTyping).display = True
        self.query_one(Chat).allow_input_submit = False

    @on(Chat.AgentResponseComplete)
    async def agent_response_complete(self, event: Chat.AgentResponseComplete) -> None:
        """Allow the user to send messages again."""
        chat = self.query_one(Chat)
        agent_is_typing = self.query_one(AgentIsTyping)
        agent_is_typing.display = False
        chat.allow_input_submit = True
        log.debug(
            f"Agent response complete. Adding message "
            f"to chat_id {event.chat_id!r}: {event.message}"
        )
        last_ai_message = event.message.message.get("content", "")
        if self.genie.runtime_config.current_state == States.BEHAVIOUR_PLANNING:
            self.genie.runtime_config = self.genie.runtime_config.copy(
                update={"behaviour_plan": str(last_ai_message)}
            )
        elif self.genie.runtime_config.current_state == States.BEHAVIOUR_GENERATION:
            self.genie.runtime_config = self.genie.runtime_config.copy(
                update={"behaviour_code": str(last_ai_message)}
            )
        elif self.genie.runtime_config.current_state == States.ROUNDS_PLANNING:
            self.genie.runtime_config = self.genie.runtime_config.copy(
                update={"rounds_plan": str(last_ai_message)}
            )
        elif self.genie.runtime_config.current_state == States.ROUNDS_GENERATION:
            self.genie.runtime_config = self.genie.runtime_config.copy(
                update={"rounds_code": str(last_ai_message)}
            )
        else:
            raise Exception("Invalid state")
        app = cast("ServiceEngine", self.app)
        app.runtime_config = self.genie.runtime_config

    def action_next_step(self) -> None:
        if self.genie.runtime_config.current_state == States.BEHAVIOUR_PLANNING:
            self.genie.runtime_config = self.genie.runtime_config.copy(
                update={"current_state": States.BEHAVIOUR_GENERATION}
            )
        elif self.genie.runtime_config.current_state == States.BEHAVIOUR_GENERATION:
            if self.genie.runtime_config.rounds_available:
                self.genie.runtime_config = self.genie.runtime_config.copy(
                    update={"current_state": States.ROUNDS_PLANNING}
                )
            else:
                self.genie.runtime_config = self.genie.runtime_config.copy(
                    update={"current_state": States.SKILL_SELECTION}
                )
        elif self.genie.runtime_config.current_state == States.ROUNDS_PLANNING:
            self.genie.runtime_config = self.genie.runtime_config.copy(
                update={"current_state": States.ROUNDS_GENERATION}
            )
        elif self.genie.runtime_config.current_state == States.ROUNDS_GENERATION:
            self.genie.runtime_config = self.genie.runtime_config.copy(
                update={"current_state": States.SKILL_SELECTION}
            )
        app = cast("ServiceEngine", self.app)
        app.runtime_config = self.genie.runtime_config
        self.app.pop_screen()


class ScaffoldChatScreen(Screen[None]):
    AUTO_FOCUS = "ChatPromptInput"
    BINDINGS = [
        Binding(
            key="escape",
            action="app.focus('prompt')",
            description="Focus prompt",
            key_display="esc",
        ),
    ]

    def __init__(
        self,
        chat_data: ChatData,
    ):
        super().__init__()
        self.chat_data = chat_data
        # self.chats_manager = ChatsManager()

    def compose(self) -> ComposeResult:
        yield ScaffoldChat(self.chat_data)
        yield Footer()

    @on(Chat.AgentResponseStarted)
    def start_awaiting_response(self) -> None:
        """Prevent sending messages because the agent is typing."""
        self.query_one(AgentIsTyping).display = True
        self.query_one(Chat).allow_input_submit = False

    @on(Chat.AgentResponseComplete)
    async def agent_response_complete(self, event: Chat.AgentResponseComplete) -> None:
        """Allow the user to send messages again."""
        chat = self.query_one(Chat)
        agent_is_typing = self.query_one(AgentIsTyping)
        agent_is_typing.display = False
        chat.allow_input_submit = True
        log.debug(
            f"Agent response complete. Adding message "
            f"to chat_id {event.chat_id!r}: {event.message}"
        )

    # await self.chats_manager.add_message_to_chat(
    #     chat_id=self.chat_data.id, message=event.message
    # )
