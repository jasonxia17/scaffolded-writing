from enum import Enum, auto, unique
import itertools
import json
from typing import Dict, Sequence, Tuple


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

    PREPOSITION_OBJECT = auto()
    # This is the part of the original problem that the subproblem is focused on
    # e.g. a prefix, suffix, subarray, subtree, etc.

    TRAVEL_ORIGIN = auto()
    TRAVEL_DESTINATION = auto()
    PUNCTUATION = auto()

    UNDER_THE_CONSTRAINT_THAT = auto()

    CONSTRAINED_QUANTITY = auto()
    CONSTRAINT_COMPARISON_OPERATOR = auto()
    CONSTRAINT_RHS = auto()


def concatenate(
    prefixes: Sequence[str], suffixes: Sequence[str], separator=" "
) -> Tuple[str, ...]:
    return tuple(map(separator.join, itertools.product(prefixes, suffixes)))


fsm: Dict[State, Dict[Tuple[str, ...], State]] = {}

fsm[State.START] = {("Define",): State.FUNCTION_DECLARATION}

fsm[State.END] = {}

# TODO: populate this list with more options, to avoid giving away that
# "minimum possible cost" is the correct token later in the sentence.
possible_function_names = ("DP", "Memo") + concatenate(
    ["Min", "Max"], ["Cost", "Hotels", "Coupons"], separator=""
)

possible_function_declarations = ("the subproblem",) + concatenate(
    possible_function_names, ["(i)", "(i,j)"], separator=""
)

fsm[State.FUNCTION_DECLARATION] = {
    possible_function_declarations: State.TO_BE,
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
    ("of", "for", "in", "while"): State.PREPOSITION_OBJECT,
}

fsm[State.PREPOSITION_OBJECT] = {
    ("traveling",): State.TRAVEL_ORIGIN,
    ("i.", "i and j."): State.END,
}

possible_locations = (
    "the current location",
    "Hotel 1",
    "Hotel n",
    "Hotel i",
    "Hotel j",
    "Hotel k",
)

fsm[State.TRAVEL_ORIGIN] = {
    concatenate(["from"], possible_locations): State.TRAVEL_DESTINATION,
}

fsm[State.TRAVEL_DESTINATION] = {
    concatenate(["to"], possible_locations): State.PUNCTUATION,
}

fsm[State.PUNCTUATION] = {
    (".",): State.END,
    (",",): State.UNDER_THE_CONSTRAINT_THAT,
}

fsm[State.UNDER_THE_CONSTRAINT_THAT] = {
    ("under the constraint that",): State.CONSTRAINED_QUANTITY,
}

fsm[State.CONSTRAINED_QUANTITY] = {
    concatenate(["the"], relevant_quantities): State.CONSTRAINT_COMPARISON_OPERATOR,
}

fsm[State.CONSTRAINT_COMPARISON_OPERATOR] = {
    ("is at least", "is at most", "is exactly"): State.CONSTRAINT_RHS,
}

fsm[State.CONSTRAINT_RHS] = {
    concatenate(["0", "1", "i", "j", "k", "n"], ["."], separator=""): State.END,
}

assert fsm.keys() == set(State)

# Unroll the tuples, convert enums to int
processed_fsm: Dict[int, Dict[str, int]] = {}

for state, transition in fsm.items():
    processed_fsm[state.value] = {}

    for str_tuple, dest in transition.items():
        processed_fsm[state.value].update({string: dest.value for string in str_tuple})

fsm_json = json.dumps(processed_fsm)
