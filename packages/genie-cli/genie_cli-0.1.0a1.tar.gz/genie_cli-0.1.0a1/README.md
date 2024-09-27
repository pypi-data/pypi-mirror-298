# Genie CLI

Genie CLI is a command-line tool designed to interact with [Valory's Genie service](https://www.valory.xyz/post/propel-genie) to generate [Olas autonomous services](https://docs.autonolas.network/open-autonomy/get_started/what_is_an_agent_service/) using natural language. This tool leverages various libraries to provide a seamless experience for developers.

## Genie Signup Process
Please signup on this link to be added to the waitlist to get access credentials to run genie cli. [Valory's Genie Signup](https://www.valory.xyz/propel-genie).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Installation

To install the Genie CLI, you need to have Python 3.9 or higher. You can install the dependencies using the following command:

```sh
pipx install genie-cli
pipx ensurepath
```

## Usage

To use the Genie CLI, you can run the following command:

```sh
genie
```

This will start the CLI and you can follow the prompts to generate AEA agents.

## Project Structure

The project is organized as follows:

```
genie-cli/
├── src/
│   ├── genie_cli/
│   │   ├── prompts/
│   │   │   └── behaviour_prompts.py
│   │   ├── widgets/
│   │   │   ├── prompt_input.py
│   │   │   └── chatbox.py
│   │   └── __main__.py
├── pyproject.toml
├── README.md
└── .gitignore
```

### Key Files

- **`pyproject.toml`**: Contains project metadata and dependencies.
- **`src/genie_cli/prompts/behaviour_prompts.py`**: Contains prompt templates for generating behavior plans.
- **`src/genie_cli/widgets/prompt_input.py`**: Defines the `PromptInput` widget for user input.
- **`src/genie_cli/widgets/chatbox.py`**: Defines the `Chatbox` widget for displaying messages.

## License

This project is licensed under the Valory License. See the [LICENSE](LICENSE) file for details.
