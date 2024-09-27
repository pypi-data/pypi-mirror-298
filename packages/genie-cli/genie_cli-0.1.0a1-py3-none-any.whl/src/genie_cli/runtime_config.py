from pydantic import BaseModel, ConfigDict

from src.genie_cli.config import ServiceChatModel
from src.genie_cli.states.states import States


class RuntimeConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    selected_model: ServiceChatModel
    system_prompt: str
    service_path: str = ""
    skill_path: str = ""
    current_state: str = States.SCAFFOLDING
    previous_state: str = States.INIT_STATE
    behaviour_plan: str = ""
    behaviour_code: str = ""
    rounds_plan: str = ""
    rounds_code: str = ""
    rounds_available: bool = True
