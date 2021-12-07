from hotel_coupon_fsm import State, fsm
import inspect
import itertools
from typing import Callable, Dict, List, Optional


class Grader:
    def __init__(self, sentence: List[str]):
        self.parsed_sentence: Dict[State, str] = {state: "" for state in fsm}

        curr_state = State.START
        for token in sentence:
            # TODO: this stripping is not necessary anymore once redesigned to not use concatenate.
            self.parsed_sentence[curr_state] = token.rstrip(".,")

            for tokens, next_state in fsm[curr_state].items():
                if token in tokens:
                    curr_state = next_state
                    break
            else:
                raise Exception(f"State {curr_state} does not have a transition for token {token}.")

        print(self.parsed_sentence)

    def generate_feedback(self) -> str:
        # TODO: move list of constraints into separate get_constraints_in_order function
        constraints: List[Callable[[], Optional[str]]] = [
            self.check_output_quantity,
            self.check_extremal_modifier,
            self.check_function_declaration,
            self.check_no_undefined_variables,
            self.check_all_parameters_used,
            self.check_preposition_object,
            self.check_each_parameter_used_only_once,
            self.check_no_vague_phrases_where_there_should_be_an_explicit_parameter,
        ]

        # check, because it's easy to forget to update this list
        assert set(constraints) == {
            func
            for name, func in inspect.getmembers(self, predicate=inspect.ismethod)
            if name.startswith("check_")
        }, "Not all constraints were included in list"

        for constraint_function in constraints:
            feedback = constraint_function()
            if feedback is not None:
                return feedback

        return "Good job!"

    def check_output_quantity(self) -> Optional[str]:
        output_quantity = self.parsed_sentence[State.OUTPUT_QUANTITY]

        # TODO: get rid of magic strings; each token should only appear once in the code to avoid inconsistencies
        # due to typos, or issues where we might change one version and forget to change the other
        # stop using concatenate function so that we can directly check string equality

        if output_quantity in ("answer", "value"):
            return f'Please be more precise about what quantity the subproblem actually outputs. "{output_quantity}" is too vague.'
        elif output_quantity != "cost":
            return f'Are you sure that a subproblem which outputs "{output_quantity}" is useful for solving the original problem?'
        return None

    def check_extremal_modifier(self) -> Optional[str]:
        extremal_modifier = self.parsed_sentence[State.OUTPUT_EXTREMAL_MODIFIER]

        if extremal_modifier == "total":
            return f'What do you mean by "total cost"? Your trip can have multiple possible total costs, depending on what choices you make.'
        elif "maximum" in extremal_modifier:
            return f"Are you sure that a subproblem which tries to maximize cost is useful for solving the original problem?"
        return None

    def check_function_declaration(self) -> Optional[str]:
        function_declaration = self.parsed_sentence[State.FUNCTION_DECLARATION]

        if "(" not in function_declaration:
            return f"Your subproblem definition should declare a function with parameters that can be memoized."

        function_name = function_declaration.split("(")[0]

        if function_name != "MinCost":
            return (
                f'Are you sure that "{function_name}" is a good name for your subproblem function?'
            )

        return None

    def check_no_undefined_variables(self) -> Optional[str]:
        function_declaration = self.parsed_sentence[State.FUNCTION_DECLARATION]

        # TODO: don't hardcode function parameter names
        is_j_allowed = "(i,j)" in function_declaration
        if is_j_allowed:
            return None

        # TODO: create contains(token, var) method
        if any("j" in token.split() for token in self.parsed_sentence.values()):
            return "You referred to the variable j, which is not declared as a function parameter nor defined in the original problem."

        return None

    def check_all_parameters_used(self) -> Optional[str]:
        function_declaration = self.parsed_sentence[State.FUNCTION_DECLARATION]
        parameters = ["i"]
        if "(i,j)" in function_declaration:
            parameters.append("j")

        for param in parameters:
            if all(param not in token.split() for token in self.parsed_sentence.values()):
                return f"Your function declaration includes the parameter {param}, but your subproblem definition doesn't explain how {param} affects the output of the function."

        return None

    def check_preposition_object(self) -> Optional[str]:
        quantity = self.parsed_sentence[State.OUTPUT_QUANTITY]
        preposition = self.parsed_sentence[State.PREPOSITION]
        preposition_object = self.parsed_sentence[State.PREPOSITION_OBJECT]

        if preposition_object in ("i", "i and j"):
            return f'What exactly do you mean by "{quantity} {preposition} {preposition_object}"? Can you be more specific about what the function parameters represent in the context of your subproblem?'

        return None

    def check_each_parameter_used_only_once(self) -> Optional[str]:
        # TODO: member var for parametrized states, i.e. states where the following token may contain a parameter
        states_to_check = {
            "travel origin": State.TRAVEL_ORIGIN,
            "travel destination": State.TRAVEL_DESTINATION,
            "constraint on the number of coupons used": State.CONSTRAINT_RHS,
        }

        tokens_to_check = {
            field: self.parsed_sentence[state].split() for field, state in states_to_check.items()
        }

        for (field1, token1), (field2, token2) in itertools.combinations(
            tokens_to_check.items(), 2
        ):
            for param in ["i", "j"]:
                if param in token1 and param in token2:
                    return f"You used the parameter {param} to denote both the {field1} and the {field2}. It doesn't make sense to tie both of these to the same variable, since they aren't necessarily the same."

        return None

    def check_no_vague_phrases_where_there_should_be_an_explicit_parameter(self) -> Optional[str]:
        for phrase in ["the current location", "the number of coupons we have remaining"]:
            if any(phrase in token for token in self.parsed_sentence.values()):
                return f'You used the phrase "{phrase}", which is vague. Could you change this phrase to explicitly mention one of your function parameters, so that it\'s clear how {phrase} is related to the subproblem?'

        return None

    # check origin is Hotel 1, i, or j. sample feedback: The original problem is asking for the cost of a trip starting from Hotel 1. However, it's impossible to compute the cost of a trip starting from Hotel 1 using your subproblem.
    # desitination is Hotel n, i, or j...
    # check at least one of {origin, destination} contains variable, so it can reduce
    # "under the constraint" exists, and it's about coupons
    # "at least" is bad, and constraint_rhs should be i or j. sample feedback: The original problem is asking for the cost of a trip that uses at most k coupons. However, it's impossible to compute this using your subproblem.
    # constraint_rhs = k needs a special feedback message about failure to reduce to smaller subproblem


print(Grader(["Define", "MinCost(i)", "to be", "the", "total", "value", "."]).generate_feedback())
