ROUNDS_SYSTEM_PROMPT = """
You will be writing a rounds file for a skill in an agent service. You are an expert python programmer, with proper knowledge of autonomous agent services.

A rounds file defines the sequence of rounds that the skill will go through during its execution. Each round represents a specific state or stage in the skill's flow. The rounds file contains a class that inherits from the AbstractRound base class. This class must implement certain methods to handle the logic for each round.

Here are the key things to include in the rounds file:

1. Import the necessary modules at the top of the file, like AbstractRound, BaseSynchronizedData, etc.

2. Define a class for the rounds that inherits from AbstractRound. The class name should match the skill name.

3. Payloads are always necessary. Implement the following methods in the class only if required, otherwise handle using payloads only:
   - end_block(): Called at the end of each block. Perform any cleanup or data aggregation here.
   - check_payload(): Check if a payload is valid and return True if it should be processed.
   - process_payload(): Process an incoming payload during a round.
   - get_next_round(): Get the next round in the sequence after the current round ends.

4. In the process_payload() method, handle any payloads or events that are expected during each round. This is where the main logic for each round goes.

5. Use the synchronized_data attribute to access and modify shared data between rounds.

6. Carefully handle any timeouts, errors or unexpected events that may occur in each round.

7. Clearly define the conditions for transitioning between rounds in get_next_round().

Some best practices to keep in mind:
- Keep the rounds logic clear and focused. Each round should have a single responsibility.
- Use descriptive names for methods, variables and classes to make the code more readable.
- Add comments explaining any complex logic or calculations.
- Avoid duplicating code. Use helper methods to reuse common functionality.
- Log important events and state changes for debugging purposes.

Make sure to test the rounds code thoroughly with different scenarios to ensure it behaves as expected.

Please output the full code for the rounds file inside <rounds_code> tags. The code should be complete, executable and match the provided skill name and description.

Remember, the rounds file is a critical component of the skill that orchestrates its entire flow. Take time to design it carefully to ensure the skill executes smoothly and reliably.
"""

ROUND_PLANNER_EXAMPLE = '''
"""This module contains the data classes for the Hello World ABCI application."""

```python
from abc import ABC
from enum import Enum
from typing import Dict, List, Optional, Tuple, Type, cast

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    AppState,
    BaseSynchronizedData,
    CollectDifferentUntilAllRound,
    CollectSameUntilAllRound,
    CollectSameUntilThresholdRound,
    get_name,
)
from packages.valory.skills.hello_world_abci.payloads import (
    CollectRandomnessPayload,
    PrintMessagePayload,
    RegistrationPayload,
    ResetPayload,
    SelectKeeperPayload,
)


class Event(Enum):
    """Event enumeration for the Hello World ABCI demo."""

    DONE = "done"
    ROUND_TIMEOUT = "round_timeout"
    NO_MAJORITY = "no_majority"
    RESET_TIMEOUT = "reset_timeout"


class SynchronizedData(
    BaseSynchronizedData
):  # pylint: disable=too-many-instance-attributes
    """
    Class to represent the synchronized data.

    This state is replicated by the Tendermint application.
    """

    @property
    def printed_messages(self) -> List[str]:
        """Get the printed messages list."""

        return cast(
            List[str],
            self.db.get_strict("printed_messages"),
        )


class HelloWorldABCIAbstractRound(AbstractRound, ABC):
    """Abstract round for the Hello World ABCI skill."""

    synchronized_data_class: Type[BaseSynchronizedData] = SynchronizedData

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, self._synchronized_data)


class RegistrationRound(CollectSameUntilAllRound, HelloWorldABCIAbstractRound):
    """A round in which the agents get registered"""

    payload_class = RegistrationPayload

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Event]]:
        """Process the end of the block."""

        if self.collection_threshold_reached:
            synchronized_data = self.synchronized_data.update(
                participants=tuple(sorted(self.collection)),
                synchronized_data_class=SynchronizedData,
            )
            return synchronized_data, Event.DONE
        return None


class CollectRandomnessRound(
    CollectSameUntilThresholdRound, HelloWorldABCIAbstractRound
):
    """A round for collecting randomness"""

    payload_class = CollectRandomnessPayload
    synchronized_data_class = SynchronizedData
    done_event = Event.DONE
    no_majority_event = Event.NO_MAJORITY
    collection_key = get_name(SynchronizedData.participant_to_randomness)
    selection_key = get_name(SynchronizedData.most_voted_randomness)


class SelectKeeperRound(CollectSameUntilThresholdRound, HelloWorldABCIAbstractRound):
    """A round in a which keeper is selected"""

    payload_class = SelectKeeperPayload
    synchronized_data_class = SynchronizedData
    done_event = Event.DONE
    no_majority_event = Event.NO_MAJORITY
    collection_key = get_name(SynchronizedData.participant_to_selection)
    selection_key = get_name(SynchronizedData.most_voted_keeper_address)


class PrintMessageRound(CollectDifferentUntilAllRound, HelloWorldABCIAbstractRound):
    """A round in which the keeper prints the message"""

    payload_class = PrintMessagePayload

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Event]]:
        """Process the end of the block."""
        if self.collection_threshold_reached:
            synchronized_data = self.synchronized_data.update(
                participants=tuple(sorted(self.collection)),
                printed_messages=sorted(
                    [
                        cast(PrintMessagePayload, payload).message
                        for payload in self.collection.values()
                    ]
                ),
                synchronized_data_class=SynchronizedData,
            )
            return synchronized_data, Event.DONE
        return None


class ResetAndPauseRound(CollectSameUntilThresholdRound, HelloWorldABCIAbstractRound):
    """This class represents the base reset round."""

    payload_class = ResetPayload

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Event]]:
        """Process the end of the block."""
        if self.threshold_reached:
            return self.synchronized_data.create(), Event.DONE
        if not self.is_majority_possible(
            self.collection, self.synchronized_data.nb_participants
        ):
            return self.synchronized_data, Event.NO_MAJORITY
        return None


class HelloWorldAbciApp(AbciApp[Event]):
    """HelloWorldAbciApp

    Initial round: RegistrationRound

    Initial states: {RegistrationRound}

    Transition states:
        0. RegistrationRound
            - done: 1.
        1. CollectRandomnessRound
            - done: 2.
            - no majority: 1.
            - round timeout: 1.
        2. SelectKeeperRound
            - done: 3.
            - no majority: 0.
            - round timeout: 0.
        3. PrintMessageRound
            - done: 4.
            - round timeout: 0.
        4. ResetAndPauseRound
            - done: 1.
            - no majority: 0.
            - reset timeout: 0.

    Final states: {}

    Timeouts:
        round timeout: 30.0
        reset timeout: 30.0
    """

    initial_round_cls: AppState = RegistrationRound
    transition_function: AbciAppTransitionFunction = {
        RegistrationRound: {
            Event.DONE: CollectRandomnessRound,
        },
        CollectRandomnessRound: {
            Event.DONE: SelectKeeperRound,
            Event.NO_MAJORITY: CollectRandomnessRound,
            Event.ROUND_TIMEOUT: CollectRandomnessRound,
        },
        SelectKeeperRound: {
            Event.DONE: PrintMessageRound,
            Event.NO_MAJORITY: RegistrationRound,
            Event.ROUND_TIMEOUT: RegistrationRound,
        },
        PrintMessageRound: {
            Event.DONE: ResetAndPauseRound,
            Event.ROUND_TIMEOUT: RegistrationRound,
        },
        ResetAndPauseRound: {
            Event.DONE: CollectRandomnessRound,
            Event.NO_MAJORITY: RegistrationRound,
            Event.RESET_TIMEOUT: RegistrationRound,
        },
    }
    event_to_timeout: Dict[Event, float] = {
        Event.ROUND_TIMEOUT: 30.0,
        Event.RESET_TIMEOUT: 30.0,
    }
```
<code plan>
### Code Plan for `rounds.py` File

#### 1. `Event` Enum
- **Description:** Defines the various events that can occur within the HelloWorldAbciApp FSM.
- **Plan:**
  - Define all possible events such as `DONE`, `ROUND_TIMEOUT`, `NO_MAJORITY`, `RESET_TIMEOUT`.

#### 2. `SynchronizedData` Class
- **Description:** Represents the synchronized data that is replicated by the Tendermint application.
- **Plan:**
  - **Property `printed_messages`:**
    - Retrieve the list of printed messages from the database.

#### 3. `HelloWorldABCIAbstractRound` Class
- **Description:** Abstract round class for the Hello World ABCI skill, providing common properties and methods.
- **Plan:**
  - **Attribute `synchronized_data_class`:**
    - Set this to `SynchronizedData`.
  - **Property `synchronized_data`:**
    - Return the synchronized data, ensuring all agents have a consistent view of the data.

#### 4. `RegistrationRound` Class
- **Description:** Manages the registration process of agents.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `RegistrationPayload`.
  - **Method `end_block()`:**
    - Check if the collection threshold is reached.
    - If reached, update synchronized data with participants and transition to the `DONE` event.
    - If not reached, do nothing and continue the round.

#### 5. `CollectRandomnessRound` Class
- **Description:** Manages the collection of randomness.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `CollectRandomnessPayload`.
  - **Attribute `synchronized_data_class`:**
    - Set this to `SynchronizedData`.
  - **Attribute `done_event`:**
    - Set this to `Event.DONE`.
  - **Attribute `no_majority_event`:**
    - Set this to `Event.NO_MAJORITY`.
  - **Attribute `collection_key`:**
    - Set this to the name of the participant to randomness collection.
  - **Attribute `selection_key`:**
    - Set this to the name of the most voted randomness.

#### 6. `SelectKeeperRound` Class
- **Description:** Manages the selection of a keeper agent.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `SelectKeeperPayload`.
  - **Attribute `synchronized_data_class`:**
    - Set this to `SynchronizedData`.
  - **Attribute `done_event`:**
    - Set this to `Event.DONE`.
  - **Attribute `no_majority_event`:**
    - Set this to `Event.NO_MAJORITY`.
  - **Attribute `collection_key`:**
    - Set this to the name of the participant to selection collection.
  - **Attribute `selection_key`:**
    - Set this to the name of the most voted keeper address.

#### 7. `PrintMessageRound` Class
- **Description:** Manages the printing of the message by the keeper.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `PrintMessagePayload`.
  - **Method `end_block()`:**
    - Check if the collection threshold is reached.
    - If reached, update synchronized data with participants and printed messages, and transition to the `DONE` event.
    - If not reached, do nothing and continue the round.

#### 8. `ResetAndPauseRound` Class
- **Description:** Manages the reset and pause process.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `ResetPayload`.
  - **Method `end_block()`:**
    - Check if the threshold is reached.
    - If reached, reset synchronized data and transition to the `DONE` event.
    - If a majority is not possible, transition to the `NO_MAJORITY` event.
    - If neither condition is met, do nothing and continue the round.

#### 9. `HelloWorldAbciApp` Class
- **Description:** Defines the FSM for the HelloWorldAbciApp, managing state transitions and overall application behavior.
- **Plan:**
  - **Attribute `initial_round_cls`:**
    - Set this to `RegistrationRound`.
  - **Attribute `transition_function`:**
    - Define the state transitions based on events, mapping each event to the corresponding next state.
  - **Attribute `event_to_timeout`:**
    - Define timeouts for specific events such as `ROUND_TIMEOUT` and `RESET_TIMEOUT`.

### Summary
The `rounds.py` file defines the FSM for the `hello_world_abci` skill, including events, synchronized data, and state transitions. The classes manage specific stages such as agent registration, randomness collection, keeper selection, message printing, and resetting. The FSM ensures proper state transitions, handling errors, and synchronizing data across agents, facilitating the overall operation of the skill.
</code plan>

<description>
Description
Schema for code solution:

The provided code defines the FSM rounds for the hello_world skill, ensuring proper state transitions and data synchronization across agents. Each class handles specific stages, from agent registration to randomness collection, keeper selection, message printing, and state resetting. The HelloWorldAbciApp class manages the overall FSM transitions, ensuring smooth operation of the autonomous agents.
</description>
'''

ROUND_PLANNER_USER_MESSAGE = """
Please create a code plan for the rounds file of the below mentioned skill description using the code tempelate file provided below.
<skill description>
{skill_description}
</skill description>

<code template>
{code_content}
</code template>

### EXAMPLE 1:
{planner_example}

Things to consider:
- Only return the plan for the rounds file, not the entire code.
"""

ROUND_TASK_DESCRIPTION = """
Here is the rounds python file with the round classes and AbciApp already defined:

<rounds_file>
{{code_content}}
</rounds_file>

### <base_sync_data_class>
{{base_sync_data_class}}
</base_sync_data_class>

Your task is to fill in the code for each of the rounds in the provided rounds file to meet the requirements laid out in the skill specification.

Before proceeding, please go through the behaviour code of this skill, that will help you in filling the 'SynchronizedData' Class:
    <behaviour_code>
    {{behaviour_code}}
    </behaviour_code>


In each round, make sure to subclass from the appropriate base round class based on the needed functionality:
- Use CollectSameUntilThresholdRound when you want to collect the same value from the agents.
- Use CollectDifferentUntilThresholdRound when you want to collect a different value from each one of the agents.
- Use OnlyKeeperSendsRound when only one agent is expected to share a payload.
- Use VotingRound when the agents should vote on a decision, i.e., the payload is a boolean value (or None).
- Use DegenerateRound when the round is terminal for the FSM.

### Instructions
- Each round class will already have their appropriate subclass defined.
- Use the <base_sync_data_class> tag to refer to the base synchronized data class. This will help you in filling in the correct synchronized data class for each round if required.
- Make sure to define the payload_class, synchronized_data_class, events, and collection_key properly for each round based on what data needs to be shared and collected in that round.
- After implementing all the rounds, define the transition_function in the AbciApp class to wire the rounds together to enable the flow required by the skill.
- Also specify any db_pre_conditions and db_post_conditions on the database that need to be satisfied before entering and after leaving each round.

Please put the final completed rounds file code with all your implementations inside <completed_rounds_file> tags.
"""


ROUNDS_EXAMPLE_1 = """
The below mentioned code is from the behaviour file of a skill name "CeramicWriteABCI".

{round_example_1}

Overview
### Code Plan for `rounds.py` File

#### 1. `Event` Enum
- **Description:** Defines the various events that can occur within the CeramicWriteAbciApp FSM.
- **Plan:**
  - Define all possible events such as `API_ERROR`, `DONE`, `DONE_FINISHED`, `DONE_CONTINUE`, `DID_NOT_SEND`, `ROUND_TIMEOUT`, `NO_MAJORITY`, `VERIFICATION_ERROR`, `MAX_RETRIES_ERROR`.

#### 2. `SynchronizedData` Class
- **Description:** Represents the synchronized data that is replicated by the Tendermint application.
- **Plan:**
  - **Property `most_voted_randomness_round`:**
    - Retrieve the most voted randomness round from the database.
  - **Property `write_data`:**
    - Retrieve the data to be written from the database.
  - **Property `write_index`:**
    - Retrieve the current write index from the database.
  - **Property `stream_id_to_verify`:**
    - Retrieve the stream ID that needs to be verified.
  - **Property `write_results`:**
    - Retrieve the results of the write operations from the database.
  - **Property `api_retries`:**
    - Retrieve the number of API retries from the database.
  - **Property `is_data_on_sync_db`:**
    - Check if the data is on the synchronized database.

#### 3. `RandomnessRound` Class
- **Description:** Manages the generation of randomness.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `RandomnessPayload`.
  - **Attribute `synchronized_data_class`:**
    - Set this to `SynchronizedData`.
  - **Attribute `done_event`:**
    - Set this to `Event.DONE`.
  - **Attribute `no_majority_event`:**
    - Set this to `Event.NO_MAJORITY`.
  - **Attribute `collection_key`:**
    - Set this to the name of the participant to randomness collection.
  - **Attribute `selection_key`:**
    - Set this to the names of the most voted randomness round and randomness.

#### 4. `SelectKeeperRound` Class
- **Description:** Manages the selection of a keeper agent.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `SelectKeeperPayload`.
  - **Attribute `synchronized_data_class`:**
    - Set this to `SynchronizedData`.
  - **Attribute `done_event`:**
    - Set this to `Event.DONE`.
  - **Attribute `no_majority_event`:**
    - Set this to `Event.NO_MAJORITY`.
  - **Attribute `collection_key`:**
    - Set this to the name of the participant to selection collection.
  - **Attribute `selection_key`:**
    - Set this to the name of the most voted keeper address.

#### 5. `StreamWriteRound` Class
- **Description:** Manages the writing of data to a stream by the keeper.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `StreamWritePayload`.
  - **Attribute `synchronized_data_class`:**
    - Set this to `SynchronizedData`.
  - **Method `end_block()`:**
    - Check if the keeper's payload is available.
    - Handle scenarios where the payload indicates maximum retries or API errors.
    - Update synchronized data and transition to the appropriate event.

#### 6. `VerificationRound` Class
- **Description:** Manages the verification of written data.
- **Plan:**
  - **Attribute `payload_class`:**
    - Set this to `VerificationPayload`.
  - **Attribute `synchronized_data_class`:**
    - Set this to `SynchronizedData`.
  - **Method `end_block()`:**
    - Check if the threshold for verification is reached.
    - Handle verification errors and update synchronized data accordingly.
    - Determine if additional data needs to be written or if the process is finished.
    - Handle scenarios where no majority is possible.

#### 7. `FinishedVerificationRound` Class
- **Description:** Represents the final state when verification is finished.
- **Plan:**
  - Inherit from `DegenerateRound`.

#### 8. `FinishedMaxRetriesRound` Class
- **Description:** Represents the final state when maximum retries are reached.
- **Plan:**
  - Inherit from `DegenerateRound`.

#### 9. `CeramicWriteAbciApp` Class
- **Description:** Defines the FSM for the CeramicWriteAbciApp, managing state transitions and overall application behavior.
- **Plan:**
  - **Attribute `initial_round_cls`:**
    - Set this to `RandomnessRound`.
  - **Attribute `initial_states`:**
    - Define the initial states, starting with `RandomnessRound`.
  - **Attribute `transition_function`:**
    - Define the state transitions based on events, mapping each event to the corresponding next state.
  - **Attribute `final_states`:**
    - Define the final states, including `FinishedVerificationRound` and `FinishedMaxRetriesRound`.
  - **Attribute `event_to_timeout`:**
    - Define timeouts for specific events.
  - **Attribute `cross_period_persisted_keys`:**
    - Define keys that persist across periods.
  - **Attribute `db_pre_conditions`:**
    - Define preconditions for database states before each round.
  - **Attribute `db_post_conditions`:**
    - Define postconditions for database states after each round.

### Summary
The `rounds.py` file defines the FSM for the `ceramic_write_abci` skill, including events, synchronized data, and state transitions. The classes manage specific stages such as generating randomness, selecting keepers, writing to streams, and verifying data. The FSM ensures proper state transitions, handling errors, and synchronizing data across agents, facilitating the overall operation of the skill.
"""
