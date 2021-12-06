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
    AFTER_EXTREMAL_WORD = auto()
    OUTPUT_QUANTITY = auto()
    PREPOSITION = auto()

    OUTPUT_QUANTITY_DISTRACTOR_1 = auto()
    OUTPUT_QUANTITY_DISTRACTOR_2 = auto()

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
    AFTER_CONSTRAINED_OBJECT = auto()


fsm: Dict[State, Dict[Tuple[str, ...], State]] = {}

fsm[State.START] = {("Define",): State.FUNCTION_DECLARATION}

fsm[State.END] = {}

fsm[State.FUNCTION_DECLARATION] = {
    (
        "the subproblem",
        "MinCost(i)",
        "MinCost(i,j)",
        "DP(i)",
        "DP(i,j)",
        "Memo(i)",
        "Memo(i,j)",
        "the subproblem",
    ): State.TO_BE,
}

fsm[State.TO_BE] = {
    ("to be",): State.THE,
}

fsm[State.THE] = {
    ("the",): State.OUTPUT_EXTREMAL_MODIFIER,
}

fsm[State.OUTPUT_EXTREMAL_MODIFIER] = {
    ("minimum", "maximum"): State.AFTER_EXTREMAL_WORD,
    ("total",): State.OUTPUT_QUANTITY,
    ("value", "cost", "answer"): State.PREPOSITION,
    ("number of",): State.OUTPUT_QUANTITY_DISTRACTOR_1,
}

fsm[State.AFTER_EXTREMAL_WORD] = {
    ("possible",): State.OUTPUT_QUANTITY,
}

fsm[State.OUTPUT_QUANTITY] = {
    ("value", "cost", "answer"): State.PREPOSITION,
    ("number of",): State.OUTPUT_QUANTITY_DISTRACTOR_1,
}

fsm[State.PREPOSITION] = {
    (".",): State.END,
    ("of", "for"): State.SUBPROBLEM_OBJECT,
}

fsm[State.OUTPUT_QUANTITY_DISTRACTOR_1] = {
    ("hotels", "coupons"): State.OUTPUT_QUANTITY_DISTRACTOR_2,
}

fsm[State.OUTPUT_QUANTITY_DISTRACTOR_2] = {
    ("used",): State.PREPOSITION,
}

fsm[State.SUBPROBLEM_OBJECT] = {
    ("traveling from",): State.TRAVEL_ORIGIN,
    ("i.", "i and j."): State.END,
}

fsm[State.TRAVEL_ORIGIN] = {
    (
        "Hotel 1",
        "Hotel n",
        "Hotel i",
        "Hotel j",
        "Hotel k",
        "the current location",
    ): State.TO,
}

fsm[State.TO] = {
    ("to",): State.TRAVEL_DESTINATION,
}

fsm[State.TRAVEL_DESTINATION] = {
    (
        "Hotel 1",
        "Hotel n",
        "Hotel i",
        "Hotel j",
        "Hotel k",
        "the current location",
    ): State.PUNCTUATION,
}

fsm[State.PUNCTUATION] = {
    (".",): State.END,
    (",",): State.UNDER_THE_CONSTRAINT_THAT,
}

fsm[State.UNDER_THE_CONSTRAINT_THAT] = {
    ("under the constraint that",): State.CONSTRAINT_COMPARISON_OPERATOR,
}

fsm[State.CONSTRAINT_COMPARISON_OPERATOR] = {
    ("all remaining",): State.CONSTRAINED_QUANTITY,
    ("at least", "at most", "exactly"): State.CONSTRAINT_RHS,
}

fsm[State.CONSTRAINT_RHS] = {
    ("0", "1", "i", "j", "k", "n"): State.CONSTRAINED_QUANTITY,
}

fsm[State.CONSTRAINED_QUANTITY] = {
    ("hotels", "coupons"): State.AFTER_CONSTRAINED_OBJECT,
}

fsm[State.AFTER_CONSTRAINED_OBJECT] = {
    ("are used.",): State.END,
}

assert fsm.keys() == set(State)

# Unroll the tuples, convert enums to int
processed_fsm: Dict[int, Dict[str, int]] = {}

for state, transition in fsm.items():
    processed_fsm[state.value] = {}

    for str_tuple, dest in transition.items():
        processed_fsm[state.value].update({string: dest.value for string in str_tuple})

fsm_json = json.dumps(processed_fsm)
