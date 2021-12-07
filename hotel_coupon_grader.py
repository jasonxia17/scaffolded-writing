from hotel_coupon_fsm import State, fsm
import inspect
from typing import Callable, Dict, List, Optional


class Grader:
    def __init__(self, sentence: List[str]):
        self.parsed_sentence: Dict[State, str] = {state: "" for state in fsm}

        curr_state = State.START
        for token in sentence:
            self.parsed_sentence[curr_state] = token.rstrip(".,")

            for tokens, next_state in fsm[curr_state].items():
                if token in tokens:
                    curr_state = next_state
                    break
            else:
                raise Exception(f"State {curr_state} does not have a transition for token {token}.")

        print(self.parsed_sentence)

    def generate_feedback(self) -> str:
        constraints: List[Callable[[], Optional[str]]] = [
            self.check_output_quantity,
            self.check_extremal_modifier,
            self.check_function_declaration,
            self.check_no_undefined_variables,
            self.check_all_parameters_used,
            self.check_preposition_object,
        ]

        # check, because it's easy to forget to update this list
        assert set(constraints) == {
            func
            for name, func in inspect.getmembers(self, predicate=inspect.ismethod)
            if name.startswith("check_")
        }

        for constraint_function in constraints:
            feedback = constraint_function()
            if feedback is not None:
                return feedback

        return "Good job!"

    def check_output_quantity(self) -> Optional[str]:
        output_quantity = self.parsed_sentence[State.OUTPUT_QUANTITY]

        if output_quantity in ("answer", "value"):
            return f'Please be more precise about what quantity the subproblem actually outputs. "{output_quantity}" is too vague.'
        elif output_quantity != "cost":
            return f'Are you sure that a subproblem which outputs "{output_quantity}" is useful for solving the original problem?'
        return None

    def check_extremal_modifier(self) -> Optional[str]:
        extremal_modifier = self.parsed_sentence[State.OUTPUT_EXTREMAL_MODIFIER]

        if extremal_modifier == "total":
            return f'What do you mean by "total cost"? There can be multiple possible total costs, depending on what choices you makes.'
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

        is_j_allowed = "(i,j)" in function_declaration
        if is_j_allowed:
            return None

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


print(Grader(["Define", "MinCost(i)", "to be", "the", "total", "value", "."]).generate_feedback())
