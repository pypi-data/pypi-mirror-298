BASE_SYNC_DATA_CLASS = '''
```python
class BaseSynchronizedData:
    """
    Class to represent the synchronized data.

    This is the relevant data constructed and replicated by the agents.
    """

    # Keys always set by default
    # `round_count` and `period_count` need to be guaranteed to be synchronized too:
    #
    # * `round_count` is only incremented when scheduling a new round,
    #    which is by definition always a synchronized action.
    # * `period_count` comes from the `reset_index` which is the last key of the `self._data`.
    #    The `self._data` keys are only updated on create, and cleanup operations,
    #    which are also meant to be synchronized since they are used at the rounds.
    default_db_keys: Set[str] = {
        "round_count",
        "period_count",
        "all_participants",
        "nb_participants",
        "max_participants",
        "consensus_threshold",
        "safe_contract_address",
    }

    def __init__(
        self,
        db: AbciAppDB,
    ) -> None:
        """Initialize the synchronized data."""
        self._db = db

    @property
    def db(self) -> AbciAppDB:
        """Get DB."""
        return self._db

    @property
    def round_count(self) -> int:
        """Get the round count."""
        return self.db.round_count

    @property
    def period_count(self) -> int:
        """Get the period count.

        Periods are executions between calls to AbciAppDB.create(), so as soon as it is called,
        a new period begins. It is useful to have a logical subdivision of the FSM execution.
        For example, if AbciAppDB.create() is called during reset, then a period will be the
        execution between resets.

        :return: the period count
        """
        return self.db.reset_index

    @property
    def participants(self) -> FrozenSet[str]:
        """Get the currently active participants."""
        participants = frozenset(self.db.get_strict("participants"))
        if len(participants) == 0:
            raise ValueError("List participants cannot be empty.")
        return cast(FrozenSet[str], participants)

    @property
    def all_participants(self) -> FrozenSet[str]:
        """Get all registered participants."""
        all_participants = frozenset(self.db.get_strict("all_participants"))
        if len(all_participants) == 0:
            raise ValueError("List participants cannot be empty.")
        return cast(FrozenSet[str], all_participants)

    @property
    def max_participants(self) -> int:
        """Get the number of all the participants."""
        return len(self.all_participants)

    @property
    def consensus_threshold(self) -> int:
        """Get the consensus threshold."""
        threshold = self.db.get_strict("consensus_threshold")
        min_threshold = consensus_threshold(self.max_participants)

        if threshold is None:
            return min_threshold

        threshold = int(threshold)
        max_threshold = len(self.all_participants)

        if min_threshold <= threshold <= max_threshold:
            return threshold

        expected_range = (
            f"can only be {min_threshold}"
            if min_threshold == max_threshold
            else f"not in [{min_threshold}, {max_threshold}]"
        )
        raise ValueError(f"Consensus threshold {threshold} {expected_range}.")

    @property
    def sorted_participants(self) -> Sequence[str]:
        """
        Get the sorted participants' addresses.

        The addresses are sorted according to their hexadecimal value;
        this is the reason we use key=str.lower as comparator.

        This property is useful when interacting with the Safe contract.

        :return: the sorted participants' addresses
        """
        return sorted(self.participants, key=str.lower)

    @property
    def nb_participants(self) -> int:
        """Get the number of participants."""
        participants = cast(List, self.db.get("participants", []))
        return len(participants)

    @property
    def slashing_config(self) -> str:
        """Get the slashing configuration."""
        return self.db.slashing_config

    @slashing_config.setter
    def slashing_config(self, config: str) -> None:
        """Set the slashing configuration."""
        self.db.slashing_config = config

    def update(
        self,
        synchronized_data_class: Optional[Type] = None,
        **kwargs: Any,
    ) -> "BaseSynchronizedData":
        """Copy and update the current data."""
        self.db.update(**kwargs)

        class_ = (
            type(self) if synchronized_data_class is None else synchronized_data_class
        )
        return class_(db=self.db)

    def create(
        self,
        synchronized_data_class: Optional[Type] = None,
    ) -> "BaseSynchronizedData":
        """Copy and update with new data. Set values are stored as sorted tuples to the db for determinism."""
        self.db.create()
        class_ = (
            type(self) if synchronized_data_class is None else synchronized_data_class
        )
        return class_(db=self.db)

    def __repr__(self) -> str:
        """Return a string representation of the data."""
        return f"{self.__class__.__name__}(db={self._db})"

    @property
    def keeper_randomness(self) -> float:
        """Get the keeper's random number [0-1]."""
        return (
            int(self.most_voted_randomness, base=16) / MAX_INT_256
        )  # DRAND uses sha256 values

    @property
    def most_voted_randomness(self) -> str:
        """Get the most_voted_randomness."""
        return cast(str, self.db.get_strict("most_voted_randomness"))

    @property
    def most_voted_keeper_address(self) -> str:
        """Get the most_voted_keeper_address."""
        return cast(str, self.db.get_strict("most_voted_keeper_address"))

    @property
    def is_keeper_set(self) -> bool:
        """Check whether keeper is set."""
        return self.db.get("most_voted_keeper_address", None) is not None

    @property
    def blacklisted_keepers(self) -> Set[str]:
        """Get the current cycle's blacklisted keepers who cannot submit a transaction."""
        raw = cast(str, self.db.get("blacklisted_keepers", ""))
        return set(textwrap.wrap(raw, ADDRESS_LENGTH))

    @property
    def participant_to_selection(self) -> DeserializedCollection:
        """Check whether keeper is set."""
        serialized = self.db.get_strict("participant_to_selection")
        deserialized = CollectionRound.deserialize_collection(serialized)
        return cast(DeserializedCollection, deserialized)

    @property
    def participant_to_randomness(self) -> DeserializedCollection:
        """Check whether keeper is set."""
        serialized = self.db.get_strict("participant_to_randomness")
        deserialized = CollectionRound.deserialize_collection(serialized)
        return cast(DeserializedCollection, deserialized)

    @property
    def participant_to_votes(self) -> DeserializedCollection:
        """Check whether keeper is set."""
        serialized = self.db.get_strict("participant_to_votes")
        deserialized = CollectionRound.deserialize_collection(serialized)
        return cast(DeserializedCollection, deserialized)

    @property
    def safe_contract_address(self) -> str:
        """Get the safe contract address."""
        return cast(str, self.db.get_strict("safe_contract_address"))
```
'''

ROUND_EXAMPLE_1_CODE = '''
```python
import json
from enum import Enum
from typing import Dict, FrozenSet, Optional, Set, Tuple, cast

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AppState,
    BaseSynchronizedData,
    CollectSameUntilThresholdRound,
    DegenerateRound,
    EventToTimeout,
    OnlyKeeperSendsRound,
    get_name,
)
from packages.valory.skills.ceramic_write_abci.payloads import (
    RandomnessPayload,
    SelectKeeperPayload,
    StreamWritePayload,
    VerificationPayload,
)


class Event(Enum):
    """CeramicWriteAbciApp Events"""

    API_ERROR = "api_error"
    DONE = "done"
    DONE_FINISHED = "done_finished"
    DONE_CONTINUE = "done_continue"
    DID_NOT_SEND = "did_not_send"
    ROUND_TIMEOUT = "round_timeout"
    NO_MAJORITY = "no_majority"
    VERIFICATION_ERROR = "verification_error"
    MAX_RETRIES_ERROR = "max_retries_error"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """

    @property
    def most_voted_randomness_round(self) -> int:  # pragma: no cover
        """Get the most voted randomness round."""
        round_ = self.db.get_strict("most_voted_randomness_round")
        return cast(int, round_)

    @property
    def write_data(self) -> list:
        """Get the write_stream_id."""
        return cast(list, self.db.get_strict("write_data"))

    @property
    def write_index(self) -> int:
        """Get the write_index."""
        return cast(int, self.db.get("write_index", 0))

    @property
    def stream_id_to_verify(self) -> str:
        """Get the stream_id_to_verify."""
        return cast(str, self.db.get_strict("stream_id_to_verify"))

    @property
    def write_results(self) -> list:
        """Get the write_results."""
        return cast(list, self.db.get("write_results", []))

    @property
    def api_retries(self) -> int:
        """Get the api_retries."""
        return cast(int, self.db.get("api_retries", 0))

    @property
    def is_data_on_sync_db(self) -> bool:
        """Get the is_data_on_sync_db."""
        return cast(bool, self.db.get("is_data_on_sync_db", True))


class RandomnessRound(CollectSameUntilThresholdRound):
    """A round for generating randomness"""

    payload_class = RandomnessPayload
    synchronized_data_class = SynchronizedData
    done_event = Event.DONE
    no_majority_event = Event.NO_MAJORITY
    collection_key = get_name(SynchronizedData.participant_to_randomness)
    selection_key = (
        get_name(SynchronizedData.most_voted_randomness_round),
        get_name(SynchronizedData.most_voted_randomness),
    )


class SelectKeeperRound(CollectSameUntilThresholdRound):
    """A round in which a keeper is selected for transaction submission"""

    payload_class = SelectKeeperPayload
    synchronized_data_class = SynchronizedData
    done_event = Event.DONE
    no_majority_event = Event.NO_MAJORITY
    collection_key = get_name(SynchronizedData.participant_to_selection)
    selection_key = get_name(SynchronizedData.most_voted_keeper_address)


class StreamWriteRound(OnlyKeeperSendsRound):
    """StreamWriteRound"""

    MAX_RETRIES_PAYLOAD = "MAX_RETRIES_PAYLOAD"

    payload_class = StreamWritePayload
    synchronized_data_class = SynchronizedData

    def end_block(
        self,
    ) -> Optional[
        Tuple[BaseSynchronizedData, Enum]
    ]:  # pylint: disable=too-many-return-statements
        """Process the end of the block."""
        if self.keeper_payload is None:
            return None

        if self.keeper_payload is None:  # pragma: no cover
            return self.synchronized_data, Event.DID_NOT_SEND

        if (
            cast(StreamWritePayload, self.keeper_payload).content
            == StreamWriteRound.MAX_RETRIES_PAYLOAD
        ):
            return self.synchronized_data, Event.MAX_RETRIES_ERROR

        keeper_payload = json.loads(
            cast(StreamWritePayload, self.keeper_payload).content
        )

        if not keeper_payload["success"]:
            api_retries = cast(SynchronizedData, self.synchronized_data).api_retries
            synchronized_data = self.synchronized_data.update(
                synchronized_data_class=SynchronizedData,
                **{
                    get_name(SynchronizedData.api_retries): api_retries + 1,
                }
            )
            return synchronized_data, Event.API_ERROR

        synchronized_data = self.synchronized_data.update(
            synchronized_data_class=SynchronizedData,
            **{
                get_name(SynchronizedData.stream_id_to_verify): keeper_payload[
                    "stream_id_to_verify"
                ],
            }
        )

        return synchronized_data, Event.DONE


class VerificationRound(CollectSameUntilThresholdRound):
    """VerificationRound"""

    payload_class = VerificationPayload
    synchronized_data_class = SynchronizedData

    ERROR_PAYLOAD = "error"
    SUCCCESS_PAYLOAD = "success"

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Event]]:
        """Process the end of the block."""
        if self.threshold_reached:
            if self.most_voted_payload == self.ERROR_PAYLOAD:
                return self.synchronized_data, Event.VERIFICATION_ERROR

            synchronized_data = cast(SynchronizedData, self.synchronized_data)
            next_write_index = synchronized_data.write_index + 1

            write_results = synchronized_data.write_results
            write_results.append(
                {"stream_id": synchronized_data.stream_id_to_verify, "verified": True}
            )

            # Check if we need to continue writing
            write_data = (
                synchronized_data.write_data
                if synchronized_data.is_data_on_sync_db
                else self.context.state.ceramic_data
            )

            if next_write_index < len(write_data):
                synchronized_data = synchronized_data.update(
                    synchronized_data_class=SynchronizedData,
                    **{
                        get_name(SynchronizedData.write_index): next_write_index,
                        get_name(SynchronizedData.write_results): write_results,
                    }
                )
                return synchronized_data, Event.DONE_CONTINUE
            else:
                # We have finished writing
                synchronized_data = synchronized_data.update(
                    synchronized_data_class=SynchronizedData,
                    **{
                        get_name(SynchronizedData.write_index): 0,  # reset the index
                        get_name(SynchronizedData.write_results): write_results,
                    }
                )
                return synchronized_data, Event.DONE_FINISHED

        if not self.is_majority_possible(
            self.collection, self.synchronized_data.nb_participants
        ):
            return self.synchronized_data, Event.NO_MAJORITY
        return None


class FinishedVerificationRound(DegenerateRound):
    """FinishedVerificationRound"""


class FinishedMaxRetriesRound(DegenerateRound):
    """FinishedMaxRetriesRound"""


class CeramicWriteAbciApp(AbciApp[Event]):
    """CeramicWriteAbciApp"""

    initial_round_cls: AppState = RandomnessRound
    initial_states: Set[AppState] = {RandomnessRound}
    transition_function: AbciAppTransitionFunction = {
        RandomnessRound: {
            Event.DONE: SelectKeeperRound,
            Event.NO_MAJORITY: RandomnessRound,
            Event.ROUND_TIMEOUT: RandomnessRound,
        },
        SelectKeeperRound: {
            Event.DONE: StreamWriteRound,
            Event.NO_MAJORITY: RandomnessRound,
            Event.ROUND_TIMEOUT: RandomnessRound,
        },
        StreamWriteRound: {
            Event.API_ERROR: RandomnessRound,
            Event.DID_NOT_SEND: RandomnessRound,
            Event.DONE: VerificationRound,
            Event.ROUND_TIMEOUT: RandomnessRound,
            Event.MAX_RETRIES_ERROR: FinishedMaxRetriesRound,
        },
        VerificationRound: {
            Event.VERIFICATION_ERROR: RandomnessRound,
            Event.DONE_CONTINUE: StreamWriteRound,
            Event.DONE_FINISHED: FinishedVerificationRound,
            Event.NO_MAJORITY: RandomnessRound,
            Event.ROUND_TIMEOUT: RandomnessRound,
        },
        FinishedVerificationRound: {},
        FinishedMaxRetriesRound: {},
    }
    final_states: Set[AppState] = {FinishedVerificationRound, FinishedMaxRetriesRound}
    event_to_timeout: EventToTimeout = {
        Event.ROUND_TIMEOUT: 30.0,
    }
    cross_period_persisted_keys: FrozenSet[str] = frozenset()
    db_pre_conditions: Dict[AppState, Set[str]] = {
        RandomnessRound: set(),
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        FinishedVerificationRound: set(),
        FinishedMaxRetriesRound: set(),
    }

```
'''
