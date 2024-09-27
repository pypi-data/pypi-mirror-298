from typing import Optional
from pydantic import BaseModel, Field


# Base model for common fields related to user information and token
class UserAuth(BaseModel):
    username: str = Field(..., alias="username", description="User name of the agent")
    token: str = Field(..., alias="token", description="Token of the login")


class Login(BaseModel):
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")


class LoginResponse(BaseModel):
    access_token: Optional[str] = Field("", alias="access_token")
    detail: str = Field("", alias="detail")


class NewBuild(UserAuth):
    author: str = Field(..., alias="author", description="Author of the build")
    name: str = Field(..., alias="name", description="Name of the agent")


class NewBuildResponse(BaseModel):
    message: str = Field(..., alias="message", description="Message of the response")
    service_idf: Optional[str] = Field(
        "", alias="service_idf", description="Id of the build"
    )


class FsmGenerator(UserAuth):
    prompt: str = Field(
        ..., alias="prompt", description="Prompt for the FSM generation"
    )
    author: str = Field(..., alias="author", description="Author of the build")
    build_id: str = Field(..., alias="build_id", description="Id of the build")
    openai_api_key: str = Field(
        ..., alias="openai_api_key", description="OpenAI API key"
    )


class FsmGeneratorResponse(BaseModel):
    message: str = Field(..., alias="message", description="Id of the FSM")
    response_idf: str = Field(
        ..., alias="response_idf", description="Id of the response"
    )


class FsmScaffold(UserAuth):
    author: str = Field(..., alias="author", description="Author of the build")
    build_id: str = Field(..., alias="build_id", description="Id of the build")


class AgentDownload(UserAuth):
    build_id: str = Field(..., alias="build_id", description="Id of the build")
    author: str = Field(..., alias="author", description="Author of the build")
