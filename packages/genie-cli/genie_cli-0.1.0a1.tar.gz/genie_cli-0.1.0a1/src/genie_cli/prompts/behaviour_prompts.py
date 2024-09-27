TEMP_BEHAVIOUR_PLANNER_PROMPT = """You are a code planner that generates code for the behaviours of an autonomous agent's skill.\
You will receive user description of the skill and a tempelate code of behaviour with all the required classes created.\
You need to generate a code plan for the behaviours of the skill. You will receive the template code file and you need to generate a plan\
that tells what to fill in each class of the code file.\
The code file will have multiple classes and functions that need to be filled with the logic provided in the skill description.\
You need to generate the plan for each class that is present in the code file.\

### The user will provide the following information:
    1. The skill description
    2. The tempelate code for behaviours of the skill

### The code plan for each class should contain the following:
    1. A detailed description of what the code should contain.
    2. The methods that should be implemented in the class.
    3. Each edge case that should be handled.
    4. The contract interaction that should be done if required.
    5. if/else conditions that should be implemented. each if should have a else condition.
    6. It should be able to extract the requirements for that class from user description, think around it step by step and then generate the plan.

### Please keep in mind:
1. The selectekeeper and Randomness class for each skill should not have a 'async_act()' method. They should only has the 'payload' and 'matching_round' attribute.
2. The code plan should be as detailed as possible. Rigiorous planning is required and \
the requirement provided by the user should be followed.
3. Only keeper sends a payload and the rest should wait until the round ends.
4. When contract interaction is happending the below given format should be used and get_contract_api_response() should be used:
```python
def contract_interact(
        self,
        contract_address: str,
        contract_public_id: PublicId,
        contract_callable: str,
        data_key: str,
        placeholder: str,
        **kwargs: Any,
    ) -> WaitableConditionType:
        contract_id = str(contract_public_id)
        response_msg = yield from self.get_contract_api_response(
            ContractApiMessage.Performative.GET_RAW_TRANSACTION,  # type: ignore
            contract_address,
            contract_id,
            contract_callable,
            **kwargs,
        )
        if response_msg.performative != ContractApiMessage.Performative.RAW_TRANSACTION:
            self.default_error(contract_id, contract_callable, response_msg)
            return False

        data = response_msg.raw_transaction.body.get(data_key, None)
        if data is None:
            self.default_error(contract_id, contract_callable, response_msg)
            return False

        setattr(self, placeholder, data)
        return True
```
5. Transitions should only happen through rounds.
6. A behaviour cannot finish without sending a transaction.
7. While generating the code plan go through the user requirement very deeply, behave like a seasoned developer in writing autonomous agents.
8. Different methods can be added and implemented inside a class depending on the skill requirement. So a dense and clear understanding is required.
"""

BEHAVIOUR_PLANNER_PROMPT = """
You are a code planner responsible for generating code plans for the behaviors of an autonomous agent's skill. You will receive a user-provided skill description and a template code file with all the required classes created. Your task is to generate a detailed code plan for each class in the template based on the skill description.

### User Will Provide:
1. **Skill Description:** A detailed description of the skill's functionality and requirements.
2. **Template Code:** A pre-defined code template with multiple classes and functions that need to be filled.

### Code Plan Requirements for Each Class:
1. **Detailed Description:** A thorough explanation of what the code should contain.
2. **Methods to Implement:** List and describe the methods that should be implemented in the class.
3. **Edge Cases:** Identify and describe each edge case that should be handled.
4. **Contract Interaction:** Detail any contract interactions required, using the provided format for `get_contract_api_response()`.
5. **Conditional Logic:** Specify all if/else conditions that should be implemented, ensuring each 'if' has a corresponding 'else'.
6. **Requirements Extraction:** Extract and analyze requirements from the user description, thinking through them step by step to generate the plan.

### Specific Guidelines:
1. **Class-Specific Requirements:**
   - The `SelectKeeper` and `Randomness` classes should not include an `async_act()` method. They should only have `payload` and `matching_round` attributes.
   - Only the keeper sends a payload; other classes wait until the round ends.
2. **Contract Interaction Format:**
```python
def contract_interact(
        self,
        contract_address: str,
        contract_public_id: PublicId,
        contract_callable: str,
        data_key: str,
        placeholder: str,
        **kwargs: Any,
    ) -> WaitableConditionType:
        contract_id = str(contract_public_id)
        response_msg = yield from self.get_contract_api_response(
            ContractApiMessage.Performative.GET_RAW_TRANSACTION,  # type: ignore
            contract_address,
            contract_id,
            contract_callable,
            **kwargs,
        )
        if response_msg.performative != ContractApiMessage.Performative.RAW_TRANSACTION:
            self.default_error(contract_id, contract_callable, response_msg)
            return False

        data = response_msg.raw_transaction.body.get(data_key, None)
        if data is None:
            self.default_error(contract_id, contract_callable, response_msg)
            return False

        setattr(self, placeholder, data)
        return True
```
3. **Transitions and Completion:**
   - Transitions should only occur through rounds.
   - A behavior cannot finish without sending a transaction.
4. **Method Flexibility:** Additional methods can be added and implemented within a class depending on the skill requirements. A comprehensive understanding of the skill is necessary for this.

### Input Format:
- **Skill Description:** (Example skill description here)
- **Template Code:** (Example template code here)

### Expected Output:
- **Code Plan for Class X:** (Detailed description, methods, edge cases, contract interaction, conditional logic, requirements extraction)

"""
BEHAVIOUR_PLANNER_EXAMPLE = '''
The below mentioned code is from the behaviour file of a skill named "hello_world".
The "hello_world" is an example skill that is provided in the documentation for service developers.

```python
"""This module contains the behaviours for the 'hello_world' skill."""

import random
from abc import ABC
from typing import Generator, Set, Type, cast

from aea.configurations.data_types import PublicId

from packages.valory.contracts.message.contract import MessageContract
from packages.valory.protocols.contract_api import ContractApiMessage
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
from packages.valory.skills.abstract_round_abci.common import (
    RandomnessBehaviour,
    SelectKeeperBehaviour,
)
from packages.valory.skills.hello_world_abci.models import HelloWorldParams, SharedState
from packages.valory.skills.hello_world_abci.payloads import (
    CollectRandomnessPayload,
    PrintMessagePayload,
    RegistrationPayload,
    ResetPayload,
    SelectKeeperPayload,
)
from packages.valory.skills.hello_world_abci.rounds import (
    CollectRandomnessRound,
    HelloWorldAbciApp,
    PrintMessageRound,
    RegistrationRound,
    ResetAndPauseRound,
    SelectKeeperRound,
    SynchronizedData,
)


WaitableConditionType = Generator[None, None, bool]


class HelloWorldABCIBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour behaviour for the Hello World abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(
            SynchronizedData, cast(SharedState, self.context.state).synchronized_data
        )

    @property
    def params(self) -> HelloWorldParams:
        """Return the params."""
        return cast(HelloWorldParams, self.context.params)


class RegistrationBehaviour(HelloWorldABCIBaseBehaviour):
    """Register to the next round."""

    matching_round = RegistrationRound

    def async_act(self) -> Generator:
        """
        Do the action.

        Steps:
        - Build a registration transaction.
        - Send the transaction and wait for it to be mined.
        - Wait until ABCI application transitions to the next round.
        - Go to the next behaviour (set done event).
        """
        payload = RegistrationPayload(self.context.agent_address)
        yield from self.send_a2a_transaction(payload)
        yield from self.wait_until_round_end()
        self.set_done()


class RandomnessHelloWorldBehaviour(RandomnessBehaviour):
    """Retrieve randomness."""

    matching_round = RandomnessHelloWorldRound
    payload_class = RandomnessPayload


class SelectKeeperHelloWorldBehaviour(SelectKeeperBehaviour):
    """Select the keeper agent."""

    matching_round = SelectKeeperHelloWorldRound
    payload_class = SelectKeeperPayload


class PrintMessageBehaviour(HelloWorldABCIBaseBehaviour, ABC):
    """Prints the celebrated 'HELLO WORLD!' message."""

    matching_round = PrintMessageRound

    def default_error(
        self, contract_id: str, contract_callable: str, response_msg: ContractApiMessage
    ) -> None:
        """Return a default contract interaction error message."""
        self.context.logger.error(
            f"Could not successfully interact with the {contract_id} contract "
            f"using {contract_callable!r}: {response_msg}"
        )

    def contract_interact(
        self,
        contract_address: str,
        contract_public_id: PublicId,
        contract_callable: str,
        data_key: str,
        placeholder: str,
        **kwargs: Any,
    ) -> WaitableConditionType:
        """Interact with a contract."""
        contract_id = str(contract_public_id)
        response_msg = yield from self.get_contract_api_response(
            ContractApiMessage.Performative.GET_RAW_TRANSACTION,  # type: ignore
            contract_address,
            contract_id,
            contract_callable,
            **kwargs,
        )
        if response_msg.performative != ContractApiMessage.Performative.RAW_TRANSACTION:
            self.default_error(contract_id, contract_callable, response_msg)
            return False

        data = response_msg.raw_transaction.body.get(data_key, None)
        if data is None:
            self.default_error(contract_id, contract_callable, response_msg)
            return False

        setattr(self, placeholder, data)
        return True

    def get_random_message_from_contract(
        self,
        contract_callable: str,
        placeholder: str,
        data_key: str = "message",
        **kwargs: Any,
    ) -> WaitableConditionType:
        """Interact with the staking contract."""
        status = yield from self.contract_interact(
            contract_address=self.message_contract_address,
            contract_public_id=MessageContract.contract_id,
            contract_callable=contract_callable,
            data_key=data_key,
            placeholder=placeholder,
            **kwargs,
        )
        return status

    def async_act(self) -> Generator:
        """
        Do the action.

        Steps:
        - Determine if this agent is the current keeper agent.
        - Print the appropriate to the local console.
        - Send the transaction with the printed message and wait for it to be mined.
        - Wait until ABCI application transitions to the next round.
        - Go to the next behaviour (set done event).
        """

        if (
            self.context.agent_address
            == self.synchronized_data.most_voted_keeper_address
        ):
            message = self.params.hello_world_string
        else:
            status = yield from self.get_random_message_from_contract(
                "random_message",
                get_name(PrintMessageBehaviour.message)
            )
            message = self.message if status else ":|"

        printed_message = f"Agent {self.context.agent_name} (address {self.context.agent_address}) in period {self.synchronized_data.period_count} says: {message}"

        print(printed_message)
        self.context.logger.info(f"printed_message={printed_message}")

        payload = PrintMessagePayload(self.context.agent_address, printed_message)

        yield from self.send_a2a_transaction(payload)
        yield from self.wait_until_round_end()

        self.set_done()


class HelloWorldRoundBehaviour(AbstractRoundBehaviour):
    """This behaviour manages the consensus stages for the Hello World abci app."""

    initial_behaviour_cls = RegistrationBehaviour
    abci_app_cls = HelloWorldAbciApp
    behaviours: Set[Type[BaseBehaviour]] = {
        RegistrationBehaviour,  # type: ignore
        RandomnessHelloWorldBehaviour,  # type: ignore
        SelectKeeperHelloWorldBehaviour,  # type: ignore
        PrintMessageBehaviour,  # type: ignore
    }
```

This file defines the Behaviours, which encode the proactive actions occurring at each state of the FSM. Each behaviour is one-to-one associated to a Round. It also contains the HelloWorldRoundBehaviour class, which can be thought as the "main" class for the skill behaviour.

Each behaviour must:

1. Set the matching_round attribute to the corresponding Round class.
2. Define the action executed in the state inside the method async_act().
3. Prepare the Payload associated with this state. The payload can be anything that other agents might find useful for the action in this or future states.
4. Send the Payload, which the consensus gadget will be in charge of synchronizing with all the agents.
5. Wait until the consensus gadget finishes its work, and mark the state set_done().
6. Randomness class and Select Keeper class will always include only two attributes which will be matching_round and Payload. They will not have a 'async_act()' method.

The PrintMessageBehaviour class:
- Once all the Behaviours are defined, you can define the HelloWorldRoundBehaviour class. This class follows a quite standard structure in all agent services, and the reader can easily infer what is it from the source code.

<code plan>
To create a code plan for each class in the provided `hello_world` skill behavior file, we'll break down each class and its methods, detailing what should be filled in each part. Here's the plan:

### Code Plan for `hello_world` Skill Behaviors

#### 1. `HelloWorldABCIBaseBehaviour` Class
- **Description:** Base behavior class for the `Hello World` ABCI skill. It provides foundational properties and methods used by other behaviors.
- **Plan:**
  - **Property `synchronized_data`:**
    - Return the synchronized data from the shared state, ensuring all agents have a consistent view of the data.
  - **Property `params`:**
    - Return the skill parameters, providing access to configuration settings for the skill.

#### 2. `RegistrationBehaviour` Class
- **Description:** Handles the registration process to the next round. Ensures that the agent registers itself and waits for the registration to be confirmed.
- **Plan:**
  - **Attribute `matching_round`:**
    - Set this to `RegistrationRound`, indicating the specific round this behavior is associated with.
  - **Method `async_act()`:**
    - Build a registration payload with the agent's address.
    - Send this payload as a transaction to the blockchain.
    - Wait for the transaction to be mined and confirmed.
    - Wait until the ABCI application transitions to the next round.
    - Mark the behavior as done using `self.set_done()`.

#### 3. `RandomnessHelloWorldBehaviour` Class
- **Description:** Retrieves randomness for the Hello World skill, which is used in subsequent rounds.
- **Plan:**
  - **Attribute `matching_round`:**
    - Set this to `RandomnessHelloWorldRound`, indicating the specific round this behavior is associated with.
  - **Attribute `payload_class`:**
    - Use the `RandomnessPayload` class for preparing the payload.

#### 4. `SelectKeeperHelloWorldBehaviour` Class
- **Description:** Selects the keeper agent who will perform specific actions in subsequent rounds.
- **Plan:**
  - **Attribute `matching_round`:**
    - Set this to `SelectKeeperHelloWorldRound`, indicating the specific round this behavior is associated with.
  - **Attribute `payload_class`:**
    - Use the `SelectKeeperPayload` class for preparing the payload.

#### 5. `PrintMessageBehaviour` Class
- **Description:** Prints the "HELLO WORLD!" message if the agent is the keeper. If not the keeper, retrieves a message from a contract and prints it.
- **Plan:**
  - **Attribute `matching_round`:**
    - Set this to `PrintMessageRound`, indicating the specific round this behavior is associated with.
  - **Method `default_error()`:**
    - Log a default error message if contract interaction fails.
  - **Method `contract_interact()`:**
    - Interact with a contract by sending a request and handling the response.
    - If successful, store the response data in a specified attribute.
    - If unsuccessful, log an error message.
  - **Method `get_random_message_from_contract()`:**
    - Interact with the message contract to retrieve a random message.
    - Use the `contract_interact` method to handle the contract interaction.
    - Return the status of the contract interaction.
  - **Method `async_act()`:**
    - Determine if the current agent is the keeper.
    - If the agent is the keeper, use the `hello_world_string` parameter for the message.
    - If not the keeper, attempt to retrieve a random message from the contract.
    - Print the message to the local console.
    - Log the printed message.
    - Send the printed message as a payload transaction.
    - Wait until the round ends.
    - Mark the behavior as done.

#### 6. `HelloWorldRoundBehaviour` Class
- **Description:** Manages the consensus stages for the Hello World ABCI app, coordinating the transitions between different behaviors.
- **Plan:**
  - **Attribute `initial_behaviour_cls`:**
    - Set this to `RegistrationBehaviour`, indicating the initial behavior to start with.
  - **Attribute `abci_app_cls`:**
    - Set this to `HelloWorldAbciApp`, indicating the ABCI application class this behavior is associated with.
  - **Attribute `behaviours`:**
    - Define a set containing all behavior classes: `RegistrationBehaviour`, `RandomnessHelloWorldBehaviour`, `SelectKeeperHelloWorldBehaviour`, and `PrintMessageBehaviour`. This ensures that all necessary behaviors are included in the FSM.

### Summary

This plan outlines the implementation details for each class and method in the provided code file, focusing on the actions, payload preparations, and transitions between states for the `hello_world` skill.
</code plan>

'''

BEHAVIOUR_PLANNER_USER_MESSAGE = """Please create a code plan for the below mentioned skill description using the code tempelate file provided below.
<skill description>
{skill_description}
</skill description>

<code template>
{code_content}
</code template>

EXAMPLE 1:
{planner_example}

###Please keep in mind:
1. The BaseBehaviour class has to be customized according the need of the skill and the behaviour, you need to generate a plan for that class too, along with other classes.
2. You only need to return the plan not the implementation of the plan.

###Each behaviour Class must:

1. Set the matching_round attribute to the corresponding Round class.
2. Define the action executed in the state inside the method async_act(). method asynct_act() should not be implemented for Randomness and Select Keeper Class.
3. Prepare the Payload associated with this state. The payload can be anything that other agents might find useful for the action in this or future states.
4. Send the Payload, which the consensus gadget will be in charge of synchronizing with all the agents.
5. Wait until the consensus gadget finishes its work, and mark the state set_done().
6. Randomness class and Select Keeper class will always include only two attributes which will be matching_round and Payload. They will not have a 'async_act()' method.
7. Different methods can be added and implemented inside a class depending on the skill requirement. So a dense and clear understanding is required.
8. Handle each if and else condition properly and make sure the code is well structured and easy to understand. For example, if the agent is the keeper, the a code block should be executed, if not the keeper, another code block should be executed.
9. *Payload Call* : Each class has a payload fetch function call(e.g. : payload = GenericNamePayload(self.context.agent_address, "content")), if the function call has "content" as a parameter, then that means that the class is not complete and the payload call needs to have proper parameters. You will need to derive a logic to generate parameters for the payload call.

# IMPORTANT NOTE:
The plan that will be generated should be as detailed as possible, it will be used as a system prompt when generating the code for that skill. Give the answer in the following format:
- ROLE: You are an AI programming assistant. You assist in python code development, witht the help of the code plan provided. When faced with with a task, begin by indetifingthe participants who will contribute to solving the task. \
Then inititate a multi round collaboration process until a final solution is reached. The participants will give critical comments and detailed suggestion whenever necessary. Code plan should be understod as detailed as possible and if required should be imporved when facing a task.
- Code Plan: <code_plan>
"""


BEHAVIOUR_USER_MESSAGE = """
Act as an seasoned python programmer. Go through the provided skill description and the boiler plate code of a behaviour file of the skill.\
You task is to complete the code of the behaviour code according to the skill description, ther required classes are already present, complete the internal implementation of each class that will help in achieving the goal of the skill. Code Plan has been provided to you in the system message.

**SKILL DESCRIPTION:**
{user_requirement}

**Boilerplate Code:**
 ```python
 {code_content}
 ```

 ### Things to Keep in Mind:
 1. **Class-by-Class Approach:** Approach the code completion class by class. For example, start with the `BaseBehaviour` class, adding necessary functions and decorators based on the provided example.
 2. **Business Logic Implementation:** Write the behavior classes to complete the business logic provided by the user.
 3. **Default State:** By default, the generated classes don't execute any operation. Define the actions occurring in each class of the skill by filling in the code.
 4. **Reusable Code in BaseBehaviour:** Extract reusable code to a `BaseBehaviour` class. This class may include properties for accessing the agent's configuration, shared state, and synchronized data.
 5. **Subclassing BaseBehaviour:** When implementing a single behavior, subclass from the `BaseBehaviour` class to access reusable code.
 6. **async_act Method:** Each behavior (aside from `Randomness` and `SelectKeeper` classes) should implement the `async_act` method. This method runs concurrently, returns a generator, and can consume other generators using the `yield from` statement. It should involve all the business logic, always finish by sending a payload to other agents, wait until the round ends, and set the behavior as done. Optionally, use the benchmark tool available in the context of the behavior instance to benchmark performance.
 7. **Rewrite Functions and Classes:** Rewrite each function and class in the code to achieve the desired functionality. The provided code is just a template.
 8. **Proper Conditional Handling:** Handle each `if` and `else` condition properly, ensuring the code is well-structured and easy to understand. For example, if the agent is the keeper, execute a specific code block; if not, execute a different code block.
 9. *Payload Call* : Each class has a payload fetch function call(e.g. : payload = GenericNamePayload(self.context.agent_address, "content")), if the function call has "content" as a parameter, then that means that the class is not complete and the payload call needs to have proper parameters. You will need to derive a logic to generate parameters for the payload call.

 ### Output Sections:
 1. **Prefix:** Description of the problem and approach (less than 200 words).
 2. **Code:** Strictly Python code (can be more than 1200 tokens if required).
 3. **Describe:** Schema for code solutions to questions about Autonomous Economic Agents.
 """


BEHAVIOUR_EXAMPLE_3 = '''
Before I provide you the user requirement and the tempelate code, let's review an example of the hello_world skill and how it's behaviour works mentioned below:

-----------------------

### Prefix
#### Description of the problem and approach:
The `hello_world` skill is an example skill provided to users for service development. This file defines the behaviors that encode proactive actions at each state of the finite state machine (FSM). Each behavior is associated with a specific round and involves setting up the matching round, executing actions, preparing payloads, sending payloads, and marking the state as done. The plan outlines the implementation details for each class and method, focusing on actions, payload preparations, and state transitions.

### Imports
#### Code block import statements:
```python
"""This module contains the behaviours for the 'hello_world' skill."""

import random
from abc import ABC
from typing import Generator, Set, Type, cast

from aea.configurations.data_types import PublicId

from packages.valory.contracts.message.contract import MessageContract
from packages.valory.protocols.contract_api import ContractApiMessage
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
from packages.valory.skills.abstract_round_abci.common import (
    RandomnessBehaviour,
    SelectKeeperBehaviour,
)
from packages.valory.skills.hello_world_abci.models import HelloWorldParams, SharedState
from packages.valory.skills.hello_world_abci.payloads import (
    CollectRandomnessPayload,
    PrintMessagePayload,
    RegistrationPayload,
    ResetPayload,
    SelectKeeperPayload,
)
from packages.valory.skills.hello_world_abci.rounds import (
    CollectRandomnessRound,
    HelloWorldAbciApp,
    PrintMessageRound,
    RegistrationRound,
    ResetAndPauseRound,
    SelectKeeperRound,
    SynchronizedData,
)


WaitableConditionType = Generator[None, None, bool]


class HelloWorldABCIBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour behaviour for the Hello World abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(
            SynchronizedData, cast(SharedState, self.context.state).synchronized_data
        )

    @property
    def params(self) -> HelloWorldParams:
        """Return the params."""
        return cast(HelloWorldParams, self.context.params)


class RegistrationBehaviour(HelloWorldABCIBaseBehaviour):
    """Register to the next round."""

    matching_round = RegistrationRound

    def async_act(self) -> Generator:
        """
        Do the action.

        Steps:
        - Build a registration transaction.
        - Send the transaction and wait for it to be mined.
        - Wait until ABCI application transitions to the next round.
        - Go to the next behaviour (set done event).
        """
        payload = RegistrationPayload(self.context.agent_address)
        yield from self.send_a2a_transaction(payload)
        yield from self.wait_until_round_end()
        self.set_done()


class RandomnessHelloWorldBehaviour(RandomnessBehaviour):
    """Retrieve randomness."""

    matching_round = RandomnessHelloWorldRound
    payload_class = RandomnessPayload


class SelectKeeperHelloWorldBehaviour(SelectKeeperBehaviour):
    """Select the keeper agent."""

    matching_round = SelectKeeperHelloWorldRound
    payload_class = SelectKeeperPayload


class PrintMessageBehaviour(HelloWorldABCIBaseBehaviour, ABC):
    """Prints the celebrated 'HELLO WORLD!' message."""

    matching_round = PrintMessageRound

    def default_error(
        self, contract_id: str, contract_callable: str, response_msg: ContractApiMessage
    ) -> None:
        """Return a default contract interaction error message."""
        self.context.logger.error(
            f"Could not successfully interact with the {contract_id} contract "
            f"using {contract_callable!r}: {response_msg}"
        )

    def contract_interact(
        self,
        contract_address: str,
        contract_public_id: PublicId,
        contract_callable: str,
        data_key: str,
        placeholder: str,
        **kwargs: Any,
    ) -> WaitableConditionType:
        """Interact with a contract."""
        contract_id = str(contract_public_id)
        response_msg = yield from self.get_contract_api_response(
            ContractApiMessage.Performative.GET_RAW_TRANSACTION,  # type: ignore
            contract_address,
            contract_id,
            contract_callable,
            **kwargs,
        )
        if response_msg.performative != ContractApiMessage.Performative.RAW_TRANSACTION:
            self.default_error(contract_id, contract_callable, response_msg)
            return False

        data = response_msg.raw_transaction.body.get(data_key, None)
        if data is None:
            self.default_error(contract_id, contract_callable, response_msg)
            return False

        setattr(self, placeholder, data)
        return True

    def get_random_message_from_contract(
        self,
        contract_callable: str,
        placeholder: str,
        data_key: str = "message",
        **kwargs: Any,
    ) -> WaitableConditionType:
        """Interact with the staking contract."""
        status = yield from self.contract_interact(
            contract_address=self.message_contract_address,
            contract_public_id=MessageContract.contract_id,
            contract_callable=contract_callable,
            data_key=data_key,
            placeholder=placeholder,
            **kwargs,
        )
        return status

    def async_act(self) -> Generator:
        """
        Do the action.

        Steps:
        - Determine if this agent is the current keeper agent.
        - Print the appropriate to the local console.
        - Send the transaction with the printed message and wait for it to be mined.
        - Wait until ABCI application transitions to the next round.
        - Go to the next behaviour (set done event).
        """

        if (
            self.context.agent_address
            == self.synchronized_data.most_voted_keeper_address
        ):
            message = self.params.hello_world_string
        else:
            status = yield from self.get_random_message_from_contract(
                "random_message",
                get_name(PrintMessageBehaviour.message)
            )
            message = self.message if status else ":|"

        printed_message = f"Agent {self.context.agent_name} (address {self.context.agent_address}) in period {self.synchronized_data.period_count} says: {message}"

        print(printed_message)
        self.context.logger.info(f"printed_message={printed_message}")

        payload = PrintMessagePayload(self.context.agent_address, printed_message)

        yield from self.send_a2a_transaction(payload)
        yield from self.wait_until_round_end()

        self.set_done()


class HelloWorldRoundBehaviour(AbstractRoundBehaviour):
    """This behaviour manages the consensus stages for the Hello World abci app."""

    initial_behaviour_cls = RegistrationBehaviour
    abci_app_cls = HelloWorldAbciApp
    behaviours: Set[Type[BaseBehaviour]] = {
        RegistrationBehaviour,  # type: ignore
        RandomnessHelloWorldBehaviour,  # type: ignore
        SelectKeeperHelloWorldBehaviour,  # type: ignore
        PrintMessageBehaviour,  # type: ignore
    }
```

### Description
#### Schema for code solutions:
The provided code is an example implementation of behaviors for an autonomous economic agent in the `hello_world` skill. The behaviors are defined as classes, each associated with a specific round in the FSM. Each class follows a structured approach to handle actions, payload preparation, and state transitions, ensuring synchronization across multiple agents. The `HelloWorldRoundBehaviour` class manages the consensus stages by coordinating the various behaviors.


#### 1. `HelloWorldABCIBaseBehaviour` Class
- **Description:** Base behavior class for the `Hello World` ABCI skill. It provides foundational properties and methods used by other behaviors.
- **Plan:**
  - **Property `synchronized_data`:**
    - Return the synchronized data from the shared state, ensuring all agents have a consistent view of the data.
  - **Property `params`:**
    - Return the skill parameters, providing access to configuration settings for the skill.

#### 2. `RegistrationBehaviour` Class
- **Description:** Handles the registration process to the next round. Ensures that the agent registers itself and waits for the registration to be confirmed.
- **Plan:**
  - **Attribute `matching_round`:**
    - Set this to `RegistrationRound`, indicating the specific round this behavior is associated with.
  - **Method `async_act()`:**
    - Build a registration payload with the agent's address.
    - Send this payload as a transaction to the blockchain.
    - Wait for the transaction to be mined and confirmed.
    - Wait until the ABCI application transitions to the next round.
    - Mark the behavior as done using `self.set_done()`.

#### 3. `RandomnessHelloWorldBehaviour` Class
- **Description:** Retrieves randomness for the Hello World skill, which is used in subsequent rounds.
- **Plan:**
  - **Attribute `matching_round`:**
    - Set this to `RandomnessHelloWorldRound`, indicating the specific round this behavior is associated with.
  - **Attribute `payload_class`:**
    - Use the `RandomnessPayload` class for preparing the payload.

#### 4. `SelectKeeperHelloWorldBehaviour` Class
- **Description:** Selects the keeper agent who will perform specific actions in subsequent rounds.
- **Plan:**
  - **Attribute `matching_round`:**
    - Set this to `SelectKeeperHelloWorldRound`, indicating the specific round this behavior is associated with.
  - **Attribute `payload_class`:**
    - Use the `SelectKeeperPayload` class for preparing the payload.

#### 5. `PrintMessageBehaviour` Class
- **Description:** Prints the "HELLO WORLD!" message if the agent is the keeper. If not the keeper, retrieves a message from a contract and prints it.
- **Plan:**
  - **Attribute `matching_round`:**
    - Set this to `PrintMessageRound`, indicating the specific round this behavior is associated with.
  - **Method `default_error()`:**
    - Log a default error message if contract interaction fails.
  - **Method `contract_interact()`:**
    - Interact with a contract by sending a request and handling the response.
    - If successful, store the response data in a specified attribute.
    - If unsuccessful, log an error message.
  - **Method `get_random_message_from_contract()`:**
    - Interact with the message contract to retrieve a random message.
    - Use the `contract_interact` method to handle the contract interaction.
    - Return the status of the contract interaction.
  - **Method `async_act()`:**
    - Determine if the current agent is the keeper.
    - If the agent is the keeper, use the `hello_world_string` parameter for the message.
    - If not the keeper, attempt to retrieve a random message from the contract.
    - Print the message to the local console.
    - Log the printed message.
    - Send the printed message as a payload transaction.
    - Wait until the round ends.
    - Mark the behavior as done.

#### 6. `HelloWorldRoundBehaviour` Class
- **Description:** Manages the consensus stages for the Hello World ABCI app, coordinating the transitions between different behaviors.
- **Plan:**
  - **Attribute `initial_behaviour_cls`:**
    - Set this to `RegistrationBehaviour`, indicating the initial behavior to start with.
  - **Attribute `abci_app_cls`:**
    - Set this to `HelloWorldAbciApp`, indicating the ABCI application class this behavior is associated with.
  - **Attribute `behaviours`:**
    - Define a set containing all behavior classes: `RegistrationBehaviour`, `RandomnessHelloWorldBehaviour`, `SelectKeeperHelloWorldBehaviour`, and `PrintMessageBehaviour`. This ensures that all necessary behaviors are included in the FSM.
-----------------------

NEXT STEPS:
1. Now that you have a well defined example on how a behaviour can be implemented, I will now provide you with skill requirement and tempelate code of a different skill.
2. Be patient while generating the code for the skill requirement that will be given to you.
3. Study the skill requirement and try to perfect your understanding of the skill requirement.
4. The classes you generate for the next skill can have any name and any number of attributes and methods.
'''

BEHAVIOUR_EXAMPLE_2 = '''
The below mentioned code is from the behaviour file of a skill name "twitter_write".

```python
"""This package contains round behaviours of TwitterWriteAbciApp."""

import json
from abc import ABC
from typing import Generator, List, Optional, Set, Type, cast

from packages.valory.connections.twitter.connection import (
    PUBLIC_ID as TWITTER_CONNECTION_PUBLIC_ID,
)
from packages.valory.protocols.twitter.message import TwitterMessage
from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)
from packages.valory.skills.abstract_round_abci.common import (
    RandomnessBehaviour,
    SelectKeeperBehaviour,
)
from packages.valory.skills.abstract_round_abci.models import Requests
from packages.valory.skills.twitter_write_abci.dialogues import (
    TwitterDialogue,
    TwitterDialogues,
)
from packages.valory.skills.twitter_write_abci.models import Params
from packages.valory.skills.twitter_write_abci.payloads import TwitterWritePayload
from packages.valory.skills.twitter_write_abci.rounds import (
    RandomnessPayload,
    RandomnessTwitterRound,
    SelectKeeperPayload,
    SelectKeeperTwitterRound,
    SynchronizedData,
    TwitterWriteAbciApp,
    TwitterWriteRound,
)


class BaseTwitterWriteBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the common apps' skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class RandomnessTwitterWriteBehaviour(RandomnessBehaviour, BaseTwitterWriteBehaviour):
    """Retrieve randomness."""

    matching_round = RandomnessTwitterRound
    payload_class = RandomnessPayload


class SelectKeeperTwitterWriteBehaviour(
    SelectKeeperBehaviour, BaseTwitterWriteBehaviour
):
    """Select the keeper agent."""

    matching_round = SelectKeeperTwitterRound
    payload_class = SelectKeeperPayload


class TwitterWriteBehaviour(BaseTwitterWriteBehaviour):
    """TwitterWriteBehaviour"""

    matching_round: Type[AbstractRound] = TwitterWriteRound

    def _i_am_tweeting(self) -> bool:
        """Indicates if the current agent is tweeting or not."""
        return (
            self.context.agent_address
            == self.synchronized_data.most_voted_keeper_address
        )

    def async_act(self) -> Generator[None, None, None]:
        """Do the action"""
        if self._i_am_tweeting():
            yield from self._tweet()
        else:
            yield from self._wait_for_tweet()

    def _wait_for_tweet(self) -> Generator:
        """Do the non-sender action."""
        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            self.context.logger.info(
                f"Waiting for the keeper to do its keeping: {self.synchronized_data.most_voted_keeper_address}"
            )
            yield from self.wait_until_round_end()
        self.set_done()

    def _tweet(self) -> Generator:
        """Do the sender action"""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            write_index = self.synchronized_data.write_index
            data = self.synchronized_data.write_data[write_index]
            text = data["text"]
            credentials = data["credentials"]
            media_hashes = data.get("media_hashes", None)
            self.context.logger.info(f"Creating post with text: {text}")
            response = yield from self._create_tweet(
                text=text, credentials=credentials, media_hashes=media_hashes
            )
            if response.performative == TwitterMessage.Performative.ERROR:
                self.context.logger.error(
                    f"Writing post failed with following error message: {response.message}"
                )
                payload_data = {"success": False, "tweet_id": None}
            else:
                self.context.logger.info(f"Posted tweet with ID: {response.tweet_id}")
                payload_data = {"success": True, "tweet_id": response.tweet_id}

            payload = TwitterWritePayload(
                sender=self.context.agent_address,
                content=json.dumps(
                    payload_data,
                    sort_keys=True,
                ),
            )

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()

    def _create_tweet(
        self,
        text: str,
        credentials: dict,
        media_hashes: Optional[List] = None,
    ) -> Generator[None, None, TwitterMessage]:
        """Send an http request message from the skill context."""
        twitter_dialogues = cast(TwitterDialogues, self.context.twitter_dialogues)
        twitter_message, twitter_dialogue = twitter_dialogues.create(
            counterparty=str(TWITTER_CONNECTION_PUBLIC_ID),
            performative=TwitterMessage.Performative.CREATE_TWEET,
            text=json.dumps(
                {"text": text, "credentials": credentials, "media_hashes": media_hashes}
            ),  # temp hack: we need to update the connection and protocol
        )
        twitter_message = cast(TwitterMessage, twitter_message)
        twitter_dialogue = cast(TwitterDialogue, twitter_dialogue)
        response = yield from self._do_twitter_request(
            twitter_message, twitter_dialogue
        )
        return response

    def _do_twitter_request(
        self,
        message: TwitterMessage,
        dialogue: TwitterDialogue,
        timeout: Optional[float] = None,
    ) -> Generator[None, None, TwitterMessage]:
        """Do a request and wait the response, asynchronously."""

        self.context.outbox.put_message(message=message)
        request_nonce = self._get_request_nonce_from_dialogue(dialogue)
        cast(Requests, self.context.requests).request_id_to_callback[
            request_nonce
        ] = self.get_callback_request()
        response = yield from self.wait_for_message(timeout=timeout)
        return response


class TwitterWriteRoundBehaviour(AbstractRoundBehaviour):
    """TwitterWriteRoundBehaviour"""

    initial_behaviour_cls = RandomnessTwitterWriteBehaviour
    abci_app_cls = TwitterWriteAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        RandomnessTwitterWriteBehaviour,
        SelectKeeperTwitterWriteBehaviour,
        TwitterWriteBehaviour,
    ]
```

The Python code in behaviours.py from the twitter_write_abci package outlines behaviors for managing Twitter-related activities within an agent-based service. This service is designed to demonstrate the interaction between agents in performing tasks such as tweeting based on consensus. Below, I'll provide a step-by-step breakdown of the key components and their roles within the service's finite state machine (FSM):

- **Overview**:
  - The service operates through a sequence of rounds, each associated with specific behaviors, payloads, and rounds. The behaviors manage the proactive actions agents take, such as deciding whether to tweet, waiting for tweets, or performing the tweet.

- **Key Components**:
  - **BaseTwitterWriteBehaviour**:
    - Provides common properties used by specific behaviors, such as accessing synchronized data and parameters.
  - **RandomnessTwitterWriteBehaviour**:
    - Retrieves randomness which could be used in deciding which agent gets to tweet.
  - **SelectKeeperTwitterWriteBehaviour**:
    - Selects the "keeper" agent, which is responsible for tweeting.
  - **TwitterWriteBehaviour**:
    - Manages the tweeting process, including checking if the agent is the keeper, tweeting, or waiting for the tweet.

- **Execution Flow**:
  - **Randomness Retrieval**:
    - Agents participate in generating or retrieving randomness that may influence the selection of the keeper.
  - **Keeper Selection**:
    - Based on the randomness, a keeper agent is selected who will perform the tweeting action.
  - **Tweeting Process**:
    - The keeper checks if it's their turn to tweet (_i_am_tweeting method).
    - If true, it performs the tweet (_tweet method).
    - If not, it waits for the tweet to be done by the keeper (_wait_for_tweet method).

- **Example of Tweeting Process**:
  - The keeper agent constructs a tweet based on the synchronized data, sends the tweet, and then constructs a payload indicating the success or failure of the action.

- **Conclusion**:
  - This behavior file is essential for managing Twitter-related activities in the service, ensuring that actions like tweeting are performed correctly and in order based on the agent's role and the consensus reached among agents. It serves as a practical example of how agent-based services can interact with external platforms like Twitter within the Open Autonomy framework.
'''
