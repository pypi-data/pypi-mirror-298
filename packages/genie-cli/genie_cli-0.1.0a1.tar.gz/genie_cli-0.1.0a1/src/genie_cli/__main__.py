"""
Genie CLI
"""

import os
import tomllib
from typing import Any

import click
from click_default_group import DefaultGroup
from dotenv import load_dotenv

from rich.console import Console
from pydantic import SecretStr

from src.genie_cli.app import ServiceEngine
from src.genie_cli.config import LaunchConfig
from src.scaffolding_client.scaffold import ScaffoldConfig

from src.genie_cli.locations import config_file

load_dotenv()

console = Console()


def load_or_create_config_file() -> dict[str, Any]:
    config = config_file()

    try:
        file_config = tomllib.loads(config.read_text())
    except FileNotFoundError:
        file_config = {}
        try:
            config.touch()
        except OSError:
            pass

    return file_config


@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
def cli() -> None:
    """Interact with large language models using your terminal."""


@cli.command()
@click.argument("prompt", nargs=-1, type=str, required=False)
@click.option(
    "-m",
    "--model",
    type=str,
    default="",
    help="The model to use for the chat",
)
@click.option(
    "-i",
    "--inline",
    is_flag=True,
    help="Run in inline mode, without launching full TUI.",
    default=False,
)
def default(prompt: tuple[str, ...], model: str, inline: bool):
    prompt = prompt or ("",)
    joined_prompt = " ".join(prompt)
    # create_db_if_not_exists()
    file_config = load_or_create_config_file()
    cli_config = {}
    if model:
        cli_config["default_model"] = model

    launch_config: dict[str, Any] = {**file_config, **cli_config}
    username = os.getenv("PROPEL_USER_NAME", "admin")
    password = os.getenv("PROPEL_PASSWORD", "admin")
    openai_api_key = os.getenv("OPENAI_API_KEY", "admin")
    author = os.getenv("AUTHOR", "admin")
    app = ServiceEngine(
        LaunchConfig(**launch_config),
        ScaffoldConfig(
            username=username,
            password=SecretStr(password),
            openai_api_key=SecretStr(openai_api_key),
            author=author,
        ),
        startup_prompt=joined_prompt,
    )
    app.run(inline=inline)


if __name__ == "__main__":
    cli()
