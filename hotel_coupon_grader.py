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
        ]

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
            return

        if any("j" in token.split() for token in self.parsed_sentence.values()):
            return "You referred to the variable j, which is not declared as a function parameter nor defined in the original problem."


print(Grader(["Define", "MinCost(i)", "to be", "the", "total", "value", "."]).generate_feedback())
