from enum import Enum, auto
import json
from typing import Dict, Tuple


class State(Enum):
    START = auto()
    END = auto()

    BEFORE_DECLARE = auto()
    AFTER_DECLARE = auto()
    AFTER_TO_BE = auto()

    BEFORE_OUTPUT_QUANTITY = auto()
    AFTER_EXTREMAL_WORD = auto()
    AFTER_POSSIBLE_OR_TOTAL = auto()
    AFTER_OUTPUT_QUANTITY = auto()

    OUTPUT_QUANTITY_DISTRACTOR_1 = auto()
    OUTPUT_QUANTITY_DISTRACTOR_2 = auto()

    BEFORE_TRAVELING = auto()
    AFTER_TRAVELING = auto()

    FOR_I_DISTRACTOR = auto()
    FOR_I_AND_J_DISTRACTOR = auto()

    BEFORE_TRAVEL_ORIGIN = auto()
    AFTER_TRAVEL_ORIGIN = auto()
    BEFORE_TRAVEL_DESTINATION = auto()
    AFTER_TRAVEL_DESTINATION = auto()

    AFTER_COMMA = auto()
    AFTER_UNDER_CONSTRAINT = auto()
    BEFORE_CONSTRAINT_AMOUNT = auto()
    BEFORE_CONSTRAINED_OBJECT = auto()
    AFTER_CONSTRAINED_OBJECT = auto()


fsm: Dict[State, Dict[Tuple[str, ...], State]] = {}

fsm[State.START] = {("Define",): State.BEFORE_DECLARE}

fsm[State.BEFORE_DECLARE] = {
    (
        "the subproblem",
        "MinCost(i)",
        "MinCost(i,j)",
        "DP(i)",
        "DP(i,j)",
        "Memo(i)",
        "Memo(i,j)",
        "the subproblem",
    ): State.AFTER_DECLARE,
}

fsm[State.AFTER_DECLARE] = {
    ("to be",): State.AFTER_TO_BE,
}

fsm[State.AFTER_TO_BE] = {
    ("the",): State.BEFORE_OUTPUT_QUANTITY,
}

fsm[State.BEFORE_OUTPUT_QUANTITY] = {
    ("minimum", "maximum"): State.AFTER_EXTREMAL_WORD,
    ("total",): State.AFTER_POSSIBLE_OR_TOTAL,
    ("value", "cost", "answer"): State.AFTER_OUTPUT_QUANTITY,
    ("number of",): State.OUTPUT_QUANTITY_DISTRACTOR_1,
}

fsm[State.AFTER_EXTREMAL_WORD] = {
    ("possible",): State.AFTER_POSSIBLE_OR_TOTAL,
}

fsm[State.AFTER_POSSIBLE_OR_TOTAL] = {
    ("value", "cost", "answer"): State.AFTER_OUTPUT_QUANTITY,
    ("number of",): State.OUTPUT_QUANTITY_DISTRACTOR_1,
}

fsm[State.AFTER_OUTPUT_QUANTITY] = {
    (".",): State.END,
    ("of", "for"): State.BEFORE_TRAVELING,
}

fsm[State.OUTPUT_QUANTITY_DISTRACTOR_1] = {
    ("hotels", "coupons"): State.OUTPUT_QUANTITY_DISTRACTOR_2,
}

fsm[State.OUTPUT_QUANTITY_DISTRACTOR_2] = {
    (".",): State.OUTPUT_QUANTITY_DISTRACTOR_2,
    ("that can be used while traveling",): State.AFTER_TRAVELING,
}

# assert fsm.keys() == set(State)

# Unroll the tuples, convert enums to int
processed_fsm: Dict[int, Dict[str, int]] = {}

for state, transition in fsm.items():
    processed_fsm[state.value] = {}

    for str_tuple, dest in transition.items():
        processed_fsm[state.value].update({string: dest.value for string in str_tuple})

fsm_json = json.dumps(processed_fsm)
