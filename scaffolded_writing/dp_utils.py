from abc import abstractmethod
import itertools
from typing import Iterable, List, Optional, Set
import re
import string
from nltk.grammar import Nonterminal

from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.constraint_based_grader import Constraint
from scaffolded_writing.student_submission import StudentSubmission

POTENTIAL_VARIABLE_NAMES = set(string.ascii_lowercase) - {'a'}

class DPStudentSubmission(StudentSubmission):
    def __init__(self, token_list: List[str], cfg: ScaffoldedWritingCFG) -> None:
        super().__init__(token_list, cfg)

        self.func_name: Optional[str] = None
        self.func_params: List[str] = []

        function_declaration_subtree, = self.parse_tree.subtrees(
            filter=lambda subroot: subroot.label() == "FUNCTION_DECLARATION"
        )
        function_declaration, = function_declaration_subtree
        assert isinstance(function_declaration, str)

        match = re.fullmatch(r"(.+)\((.+)\)", function_declaration)
        if match is not None:
            self.func_name = match.group(1)
            self.func_params = match.group(2).replace(' ', '').split(',')

        # The set of all one-letter variables which are mentioned in the student's response
        # outside of the function_declaration.
        self.mentioned_variables: Set[str] = set.union(*(
            self.__extract_variables(token) for token in self.token_list if token != function_declaration
        ))

    def get_parameters_in_field(self, field_label: str) -> Set[str]:
        assert Nonterminal(field_label) in self.cfg.nonterminals

        subtrees = list(self.parse_tree.subtrees(
            filter=lambda subroot: subroot.label() == field_label
        ))
        if len(subtrees) == 0:
            return set()

        field_subtree, = subtrees

        return set.union(
            *[self.__extract_variables(leaf) for leaf in field_subtree.leaves()]
        ).intersection(self.func_params)

    def is_field_value_parameterized(self, field_label: str) -> bool:
        """
        field_label is the nonterminal that generates the field value
        """
        return len(self.get_parameters_in_field(field_label)) > 0

    @staticmethod
    def __extract_variables(token: str) -> Set[str]:
        return POTENTIAL_VARIABLE_NAMES.intersection(re.split(r"\W+", token))


class DeclareFunctionConstraint(Constraint[DPStudentSubmission]):
    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        return submission.func_name is not None

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        return "Your subproblem definition should declare a function with input parameters that can be memoized."

class CorrectOutputNounAndExtremalAdj(Constraint[DPStudentSubmission]):
    def __init__(self, correct_noun: str, correct_adj: str) -> None:
        self.correct_noun = correct_noun
        self.correct_adj = correct_adj

    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        self.is_noun_correct = submission.does_path_exist("OUTPUT_NOUN", self.correct_noun)
        self.is_adj_correct = submission.does_path_exist("EXTREMAL_ADJ", self.correct_adj)

        return self.is_noun_correct and self.is_adj_correct

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        if submission.does_path_exist("OUTPUT_NOUN", "answer"):
            return 'Please be more precise about what quantity the function actually outputs. Just saying "answer" is too vague.'

        if self.is_noun_correct and submission.does_path_exist("EXTREMAL_ADJ", "EPSILON"):
            return f'The {self.correct_noun} can vary based on what choices we make. You need to add an adjective in front of "{self.correct_noun}" in order to precisely define the output quantity of the function.'

        return "It seems like the quantity outputted by your function is not directly relevant for solving the original problem."

class DescriptiveFunctionName(Constraint[DPStudentSubmission]):
    def __init__(self, correct_func_name: str) -> None:
        self.correct_func_name = correct_func_name

    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        return submission.func_name == self.correct_func_name

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        return "Please choose a descriptive function name that accurately represents what the function outputs."

class ExplainParamsConstraint(Constraint[DPStudentSubmission]):
    def __init__(self, *, variables_in_problem: List[str]) -> None:
        self.variables_in_problem = set(variables_in_problem)

    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        self.unexplained_params = set(submission.func_params) - submission.mentioned_variables

        self.undefined_variables = submission.mentioned_variables \
            - set(submission.func_params) - self.variables_in_problem

        self.mentioned_params_without_explaining = submission.does_path_exist("MENTION_PARAMS_WITHOUT_EXPLAINING")

        return not (self.unexplained_params or self.undefined_variables or self.mentioned_params_without_explaining)

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        if self.unexplained_params:
            if len(self.unexplained_params) == 1:
                return f"Your function takes {list_to_english(sorted(self.unexplained_params))} as an input parameter, but your subproblem definition does not explain how this parameter affects the output of the function."
            else:
                return f"Your function takes {list_to_english(sorted(self.unexplained_params))} as input parameters, but your subproblem definition does not explain how these parameters affect the output of the function."

        if self.undefined_variables:
            if len(self.undefined_variables) == 1:
                return f"Your subproblem definition refers to the variable {list_to_english(sorted(self.undefined_variables))}, which is undefined. You should only refer to variables which are defined in the original problem or declared as input parameters to your function."
            else:
                return f"Your subproblem definition refers to the variables {list_to_english(sorted(self.undefined_variables))}, which are undefined. You should only refer to variables which are defined in the original problem or declared as input parameters to your function."

        if self.mentioned_params_without_explaining:
            return "Your subproblem definition mentions the function's input parameters, but it does not clearly explain how these input parameters affect the output of the function. Can you be more specific about what the function parameters represent in the context of your subproblem?"

        raise Exception("This constraint was violated but no feedback was generated.")

class DecoupledParametersConstraint(Constraint[DPStudentSubmission]):
    def __init__(self, **independent_fields: str) -> None:
        """
        independent_fields: the values in these fields should not contain the same parameters
            - key = the nonterminal assosciated with the field
            - value = an English description of the field
            (This dict should have length at least 2 in order to be meaningful.)
        """
        assert len(independent_fields) >= 2
        self.independent_fields = independent_fields

    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        for (field1, description1), (field2, description2) in itertools.combinations(
            self.independent_fields.items(), 2
        ):
            intersection = submission.get_parameters_in_field(field1).intersection(
                submission.get_parameters_in_field(field2))

            if intersection:
                self.overused_param, = intersection
                self.entangled_quantities = (description1, description2)
                return False

        return True

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        return f"You used the parameter {self.overused_param} to denote both {self.entangled_quantities[0]} and {self.entangled_quantities[1]}. It doesn't make sense to tie both of these quantities to the same parameter because these quantities can vary independently."

class CanComputeFinalAnswer(Constraint[DPStudentSubmission]):
    def __init__(self, required_feature: List[str], feedback_elaboration: str = "") -> None:
        """
        required_feature is a path that must be present in order to compute the final answer
        """
        self.required_feature = required_feature
        self.feedback_elaboration = feedback_elaboration

    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        return submission.does_path_exist(*self.required_feature)

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        return f"Your subproblem definition does not allow us to compute the final answer requested by the original problem. The problem requires that {self.feedback_elaboration}, but there is no way to impose this requirement using your subproblem definition."

class ReducesRecursivelyConstraint(Constraint[DPStudentSubmission]):
    def __init__(self, field_requiring_parameters) -> None:
        """
        field_requiring_parameterization is a field name (i.e. non-terminal) whose field value (i.e. terminal child)
        must contain a function parameter in order for the subproblem to be recursively reduced.
        """
        self.field_requiring_parameters = field_requiring_parameters

    @abstractmethod
    def get_unhandled_scenario(self, submission: DPStudentSubmission) -> str: ...

    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        return submission.is_field_value_parameterized(self.field_requiring_parameters)

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        return f"Make sure that your subproblem can be reduced to smaller instances of itself. For example, {self.get_unhandled_scenario(submission)}, but your subproblem definition does not allow us to do that."

class RestrictionImposedOnCorrectSide(Constraint[DPStudentSubmission]):
    def __init__(self, *, prefix_token: str, suffix_token: str, prefix_position: str, suffix_position: str) -> None:
        """
        irrelevant_features: terminals/non-terminals that should not appear in the student's parse tree
        """
        # TODO

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        return "... This prevents your subproblem from reducing to smaller instances of itself."

class NoIrrelevantRestrictions(Constraint[DPStudentSubmission]):
    def __init__(self, *irrelevant_features: str) -> None:
        """
        irrelevant_features: terminals/non-terminals that should not appear in the student's parse tree
        """
        self.irrelevant_features = irrelevant_features

    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        return all(not submission.does_path_exist(feature) for feature in self.irrelevant_features)

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        return "Your subproblem definition contains features or restrictions that are not relevant for solving the original problem."

class NoDoubleEndedParameterization(Constraint[DPStudentSubmission]):
    def is_satisfied(self, submission: DPStudentSubmission) -> bool:
        return not submission.does_path_exist("DOUBLE_ENDED_SUBPROBLEM")

    def get_feedback(self, submission: DPStudentSubmission) -> str:
        return "You parametrized both the start and end index of your subproblem, but for this problem, your subproblem doesn't need to reduce on both sides. Each possible choice should only cause your subproblem to get smaller on one side. Your subproblem definition might still be viable, but this slows down your algorithm by a factor of $O(n)$. (Some other problems actually do require reducing on both sides, e.g. see the Longest Palindromic Subsequence problem from lab.)"

def list_to_english(items: List[str]) -> str:
    if len(items) == 0:
        raise ValueError("Empty lists are not supported")
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        a, b = items
        return f'{a} and {b}'

    *all_but_last, last = items
    return f'{", ".join(all_but_last)}, and {last}'

def concat_into_production_rule(*iterables: Iterable[str]) -> str:
    """
    concat_into_production_rule([a1, a2, a3], [b1, b2], [c1, c2]) will return:
    "a1b1c1" | "a1b1c2" | "a1b2c1" | "a1b2c2" | ...
    """
    def wrap_in_quotes(s: str) -> str:
        if '"' not in s:
            return f'"{s}"'
        elif "'" not in s:
            return f"'{s}'"
        raise Exception(f"Cannot wrap {s} in quotes because it already contains single and double quotes.")

    rhs_possibilities = [wrap_in_quotes(''.join(tup)) for tup in itertools.product(*iterables)]
    return " | ".join(rhs_possibilities)
