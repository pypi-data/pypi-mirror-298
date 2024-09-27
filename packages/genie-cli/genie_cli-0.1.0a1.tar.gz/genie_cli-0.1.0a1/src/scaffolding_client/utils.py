import requests

from src.scaffolding_client.constants import (
    SCAFFOLDING_SERVICE_BASE_URL,
    LOGIN_ENDPOINT,
    INIT_BUILD_ENDPOINT,
    FSM_GENERATION_ENDPOINT,
    FSM_SCAFFOLDING_ENDPOINT,
    AGENT_DOWNLOAD_ENDPOINT,
)
from src.scaffolding_client.models import (
    Login,
    LoginResponse,
    NewBuild,
    NewBuildResponse,
    FsmGenerator,
    FsmGeneratorResponse,
    FsmScaffold,
    AgentDownload,
)


def login_call(username: str, password: str):
    login = Login(username=username, password=password)
    response = requests.post(
        SCAFFOLDING_SERVICE_BASE_URL + LOGIN_ENDPOINT, params=login.dict()
    )
    # response.raise_for_status()
    return LoginResponse(**response.json())


def init_build_call(username: str, token: str, author: str, name: str):
    new_build = NewBuild(username=username, token=token, author=author, name=name)

    params = {
        "user_id": new_build.username,
        "author": new_build.author,
        "name": new_build.name,
    }
    headers = {"token-verifier": new_build.token}
    response = requests.get(
        SCAFFOLDING_SERVICE_BASE_URL + INIT_BUILD_ENDPOINT,
        params=params,
        headers=headers,
    )
    response.raise_for_status()
    return NewBuildResponse(**response.json())


def fsm_generation_call(
    username: str,
    token: str,
    build_id: str,
    prompt: str,
    author: str,
    openai_api_key: str,
):
    fsm_generator = FsmGenerator(
        username=username,
        token=token,
        author=author,
        build_id=build_id,
        prompt=prompt,
        openai_api_key=openai_api_key,
    )

    params = {
        "user_id": fsm_generator.username,
        "author": fsm_generator.author,
        "response_idf": fsm_generator.build_id,
        "openai_api_key": fsm_generator.openai_api_key,
        "prompt": fsm_generator.prompt,
    }
    headers = {"token-verifier": fsm_generator.token}

    response = requests.get(
        SCAFFOLDING_SERVICE_BASE_URL + FSM_GENERATION_ENDPOINT,
        params=params,
        headers=headers,
    )
    response.raise_for_status()
    return FsmGeneratorResponse(**response.json()).message


def fsm_scaffold_call(username: str, token: str, build_id: str, author: str):
    fsm_scaffold = FsmScaffold(
        username=username, token=token, author=author, build_id=build_id
    )

    params = {
        "user_id": fsm_scaffold.username,
        "author": fsm_scaffold.author,
        "response_idf": fsm_scaffold.build_id,
    }
    headers = {"token-verifier": fsm_scaffold.token}

    response = requests.get(
        SCAFFOLDING_SERVICE_BASE_URL + FSM_SCAFFOLDING_ENDPOINT,
        params=params,
        headers=headers,
    )
    try:
        return response.json()
    except Exception as e:
        return {"Duplication error": "The build already has a scaffolded FSM."}


def agent_download_call(username: str, token: str, build_id: str, author: str):
    agent_download = AgentDownload(
        username=username, token=token, build_id=build_id, author=author
    )

    params = {
        "user_id": agent_download.username,
        "author": agent_download.author,
        "response_idf": agent_download.build_id,
    }

    headers = {"token-verifier": agent_download.token}

    with requests.get(
        SCAFFOLDING_SERVICE_BASE_URL + AGENT_DOWNLOAD_ENDPOINT,
        params=params,
        headers=headers,
        stream=True,
    ) as response:
        if response.status_code != 200:
            raise Exception(
                f"Failed to download agent: {response.content.decode('utf-8')}"
            )
        with open(f"{agent_download.build_id}.zip", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
