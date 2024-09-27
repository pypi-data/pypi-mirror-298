from pydantic import BaseModel, Field, validator, SecretStr
from src.scaffolding_client.utils import (
    login_call,
    init_build_call,
    fsm_generation_call,
    fsm_scaffold_call,
    agent_download_call,
)
import os


class ScaffoldConfig(BaseModel):
    username: str = Field(..., description="User name for authentication")
    password: SecretStr = Field(..., description="Password for authentication")
    author: str = Field(..., description="Author of the build")
    openai_api_key: SecretStr = Field(..., description="OpenAI API key")
    token: str = Field("", description="Authentication token", init=False)
    build_id: str = Field(None, description="ID of the initialized build", init=False)
    detail: str = Field("", description="Details of the login", init=False)

    @validator("username", pre=True, always=True)
    def set_username(cls, v):
        return os.getenv("PROPEL_USER_NAME", v)

    @validator("password", pre=True, always=True)
    def set_password(cls, v):
        return SecretStr(os.getenv("PROPEL_PASSWORD", v.get_secret_value()))

    @validator("author", pre=True, always=True)
    def set_author(cls, v):
        return os.getenv("AUTHOR", v)

    @validator("openai_api_key", pre=True, always=True)
    def set_openai_api_key(cls, v):
        if not v.get_secret_value().startswith("sk-"):
            raise ValueError("Invalid OpenAI API key. It must start with 'sk-'.")
        return os.getenv("OPENAI_API_KEY", v.get_secret_value())


class Scaffold:
    def __init__(self, config: ScaffoldConfig):
        self.config = config

    def login(self):
        login_response = login_call(
            self.config.username, self.config.password.get_secret_value()
        )

        if login_response.access_token:
            self.config.token = login_response.access_token
        else:
            self.config.detail = login_response.detail

    def init_build(self, name: str):
        build_response = init_build_call(
            self.config.username, self.config.token, self.config.author, name
        )

        if build_response.service_idf:
            self.config.build_id = build_response.service_idf

        return build_response.message

    async def fsm_generation(self, prompt: str):
        return fsm_generation_call(
            self.config.username,
            self.config.token,
            self.config.build_id,
            prompt,
            self.config.author,
            self.config.openai_api_key.get_secret_value(),
        )

    async def fsm_scaffold(self):
        response = fsm_scaffold_call(
            self.config.username,
            self.config.token,
            self.config.build_id,
            self.config.author,
        )

        if "Scaffolding failed" in response:
            return response["Scaffolding failed"]
        else:
            return "Scaffolding successful"

    async def agent_download(self):
        return agent_download_call(
            self.config.username,
            self.config.token,
            self.config.build_id,
            self.config.author,
        )
