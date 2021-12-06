from enum import Enum, auto, unique
import json
from typing import Dict, Tuple


@unique
class State(Enum):
    # State names describe the role played by the possible next tokens in that state
    START = auto()
    END = auto()

    FUNCTION_DECLARATION = auto()
    TO_BE = auto()
    THE = auto()

    OUTPUT_EXTREMAL_MODIFIER = auto()
    OUTPUT_QUANTITY = auto()
    PREPOSITION = auto()

    SUBPROBLEM_OBJECT = auto()
    # This is the part of the original problem that the subproblem is focused on
    # e.g. a prefix, suffix, subarray, subtree, etc.

    TRAVEL_ORIGIN = auto()
    TO = auto()
    TRAVEL_DESTINATION = auto()
    PUNCTUATION = auto()

    UNDER_THE_CONSTRAINT_THAT = auto()

    CONSTRAINED_QUANTITY = auto()
    CONSTRAINT_COMPARISON_OPERATOR = auto()
    CONSTRAINT_RHS = auto()


def concatenate():
    pass


fsm: Dict[State, Dict[Tuple[str, ...], State]] = {}

fsm[State.START] = {("Define",): State.FUNCTION_DECLARATION}

fsm[State.END] = {}

# TODO: populate this list with more options, to avoid giving away that
# "minimum possible cost" is the correct token later in the sentence.
fsm[State.FUNCTION_DECLARATION] = {
    (
        "the subproblem",
        "MinCost(i)",
        "MinCost(i,j)",
        "DP(i)",
        "DP(i,j)",
        "Memo(i)",
        "Memo(i,j)",
    ): State.TO_BE,
}

fsm[State.TO_BE] = {
    ("to be",): State.THE,
}

fsm[State.THE] = {
    ("the",): State.OUTPUT_EXTREMAL_MODIFIER,
}

fsm[State.OUTPUT_EXTREMAL_MODIFIER] = {
    ("minimum possible", "maximum possible", "total"): State.OUTPUT_QUANTITY,
}

relevant_quantities = ("cost", "number of hotels used", "number of coupons used")

fsm[State.OUTPUT_QUANTITY] = {
    ("answer", "value") + relevant_quantities: State.PREPOSITION,
}

fsm[State.PREPOSITION] = {
    (".",): State.END,
    ("of", "for", "in"): State.SUBPROBLEM_OBJECT,
}

# TODO: move "from" to later token
fsm[State.SUBPROBLEM_OBJECT] = {
    ("a trip from",): State.TRAVEL_ORIGIN,
    ("i.", "i and j."): State.END,
}

possible_locations = (
    "Hotel 1",
    "Hotel n",
    "Hotel i",
    "Hotel j",
    "Hotel k",
    "the current location",
)

fsm[State.TRAVEL_ORIGIN] = {
    possible_locations: State.TO,
}

# TODO: merge "to" into next token
fsm[State.TO] = {
    ("to",): State.TRAVEL_DESTINATION,
}

fsm[State.TRAVEL_DESTINATION] = {
    possible_locations: State.PUNCTUATION,
}

fsm[State.PUNCTUATION] = {
    (".",): State.END,
    (",",): State.UNDER_THE_CONSTRAINT_THAT,
}

fsm[State.UNDER_THE_CONSTRAINT_THAT] = {
    ("under the constraint that",): State.CONSTRAINED_QUANTITY,
}

# TODO: add "the" before quantities
fsm[State.CONSTRAINED_QUANTITY] = {
    relevant_quantities: State.CONSTRAINT_COMPARISON_OPERATOR,
}

fsm[State.CONSTRAINT_COMPARISON_OPERATOR] = {
    ("is at least", "is at most", "is exactly"): State.CONSTRAINT_RHS,
}

# TODO: add period
fsm[State.CONSTRAINT_RHS] = {
    ("0", "1", "i", "j", "k", "n"): State.END,
}

assert fsm.keys() == set(State)

# Unroll the tuples, convert enums to int
processed_fsm: Dict[int, Dict[str, int]] = {}

for state, transition in fsm.items():
    processed_fsm[state.value] = {}

    for str_tuple, dest in transition.items():
        processed_fsm[state.value].update({string: dest.value for string in str_tuple})

fsm_json = json.dumps(processed_fsm)
