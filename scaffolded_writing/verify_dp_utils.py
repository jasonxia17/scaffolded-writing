import pytest
from scaffolded_writing.dp_utils import (
    CanComputeFinalAnswer,
    CorrectOutputNounAndExtremalAdj,
    DPStudentSubmission,
    DeclareFunctionConstraint,
    DecoupledParametersConstraint,
    DescriptiveFunctionName,
    ExplainParamsConstraint,
    NoDoubleEndedParameterization,
    NoIrrelevantRestrictions,
    ReducesRecursivelyConstraint,
    concat_into_production_rule,
    list_to_english
)

from scaffolded_writing.dp_cfgs import PARTITION_SUM_CFG as cfg
from typing import List

class VerifyDPStudentSubmission:
    def verify_func_name_and_params(self) -> None:
        submission = DPStudentSubmission(
            ["define", "the subproblem", "to be the", "number of terms", "that can be obtained", "."], cfg)
        assert submission.func_name is None
        assert submission.func_params == []

        submission = DPStudentSubmission(
            ["define", "DP(i)", "to be the", "sum", "that can be obtained", "."], cfg)
        assert submission.func_name == "DP"
        assert submission.func_params == ["i"]

        submission = DPStudentSubmission(
            ["define", "MaxSum(i,j)", "to be the", "answer", "that can be obtained", "."], cfg)
        assert submission.func_name == "MaxSum"
        assert submission.func_params == ["i", "j"]

    def verify_mentioned_variables(self) -> None:
        submission = DPStudentSubmission(
            ["define", "DP(i)", "to be the", "maximum", "sum", "that can be obtained", "."], cfg)
        assert submission.mentioned_variables == set()

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[1..i]", "using", "at most", "t", "2-digit terms", "."], cfg)
        assert submission.mentioned_variables == {'i', 't'}

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[1..n]", "under the constraint that", "A[1]", "is part of a", "j-digit", "term", "."], cfg)
        assert submission.mentioned_variables == {'n', 'j'}

class VerifyDPConstraints:
    def verify_declare_function_constraint(self) -> None:
        submission = DPStudentSubmission(
            ["define", "the subproblem", "to be the", "answer", "that can be obtained", "."], cfg)
        constraint = DeclareFunctionConstraint()
        assert not constraint.is_satisfied(submission)

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "answer", "that can be obtained", "."], cfg)
        constraint = DeclareFunctionConstraint()
        assert constraint.is_satisfied(submission)

    def verify_output_noun_and_adj_constraint(self) -> None:
        submission = DPStudentSubmission(
            ["define", "the subproblem", "to be the", "answer", "that can be obtained", "."], cfg)
        constraint = CorrectOutputNounAndExtremalAdj("sum", "maximum")
        assert not constraint.is_satisfied(submission)
        assert '"answer" is too vague' in constraint.get_feedback(submission)

        submission = DPStudentSubmission(
            ["define", "the subproblem", "to be the", "number of terms", "that can be obtained", "."], cfg)
        constraint = CorrectOutputNounAndExtremalAdj("sum", "maximum")
        assert not constraint.is_satisfied(submission)
        assert "not directly relevant" in constraint.get_feedback(submission)

        submission = DPStudentSubmission(
            ["define", "the subproblem", "to be the", "sum", "that can be obtained", "."], cfg)
        constraint = CorrectOutputNounAndExtremalAdj("sum", "maximum")
        assert not constraint.is_satisfied(submission)
        assert 'add an adjective in front of "sum"' in constraint.get_feedback(submission)

        submission = DPStudentSubmission(
            ["define", "the subproblem", "to be the", "maximum", "sum", "that can be obtained", "."], cfg)
        constraint = CorrectOutputNounAndExtremalAdj("sum", "minimum")
        assert not constraint.is_satisfied(submission)
        assert "not directly relevant" in constraint.get_feedback(submission)

        constraint = CorrectOutputNounAndExtremalAdj("sum", "maximum")
        assert constraint.is_satisfied(submission)

    def verify_descriptive_function_name(self) -> None:
        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "answer", "that can be obtained", "."], cfg)
        constraint = DescriptiveFunctionName("MinSum")
        assert not constraint.is_satisfied(submission)

        submission = DPStudentSubmission(
            ["define", "MinSum(i,j)", "to be the", "answer", "that can be obtained", "."], cfg)
        constraint = DescriptiveFunctionName("MinSum")
        assert constraint.is_satisfied(submission)

    def verify_explain_params_constraint(self) -> None:
        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "using", "at most", "t", "2-digit terms", "."], cfg)
        constraint = ExplainParamsConstraint(variables_in_problem=['n'])
        assert not constraint.is_satisfied(submission)
        assert constraint.unexplained_params == {'j'}
        assert constraint.undefined_variables == {'t'}
        assert not constraint.mentioned_params_without_explaining

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained",
             "for i and j", "."], cfg)
        constraint = ExplainParamsConstraint(variables_in_problem=["n", "t"])
        assert not constraint.is_satisfied(submission)
        assert constraint.unexplained_params == set()
        assert constraint.undefined_variables == set()
        assert constraint.mentioned_params_without_explaining

        submission = DPStudentSubmission(
            ["define", "DP(i)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "using", "at most", "t", "2-digit terms", "."], cfg)
        constraint = ExplainParamsConstraint(variables_in_problem=['n', 't'])
        assert constraint.is_satisfied(submission)

    def verify_decoupled_parameters_constraint(self) -> None:
        constraint = DecoupledParametersConstraint(
            SUBARRAY="an array index",
            COMPARISON_RHS="the number of 2-digit terms",
            TERM_LENGTH="a term length",
        )

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "under the constraint that", "A[1]", "is part of a", "i-digit", "term", "."], cfg)
        assert not constraint.is_satisfied(submission)
        assert constraint.get_feedback(submission) == "You used the parameter i to denote both an array index and a term length. It doesn't make sense to tie both of these quantities to the same parameter because these quantities can vary independently."

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..j]", "using", "at most", "j", "2-digit terms", "."], cfg)
        assert not constraint.is_satisfied(submission)
        assert constraint.get_feedback(submission) == "You used the parameter j to denote both an array index and the number of 2-digit terms. It doesn't make sense to tie both of these quantities to the same parameter because these quantities can vary independently."

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "under the constraint that", "A[i]", "is part of a", "j-digit", "term", "."], cfg)
        assert constraint.is_satisfied(submission)

    def verify_can_compute_final_answer_constraint(self) -> None:
        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "under the constraint that", "A[1]", "is part of a", "j-digit", "term", "."], cfg)
        constraint = CanComputeFinalAnswer(
            ["NUM_TWO_DIGIT_TERMS_RESTRICTION", "COMPARISON_OPERATOR", "VIABLE_COMPARISON_OPERATOR"],
            "at most t 2-digit terms are used"
        )
        assert not constraint.is_satisfied(submission)
        assert constraint.get_feedback(submission) == "Your subproblem definition does not allow us to compute the final answer requested by the original problem. The problem requires that at most t 2-digit terms are used, but there is no way to impose this requirement using your subproblem definition."

        # check that comparison operator is taken into account
        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "using", "at least", "t", "2-digit terms", "."], cfg)
        assert not constraint.is_satisfied(submission)

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "using", "at most", "t", "2-digit terms", "."], cfg)
        assert constraint.is_satisfied(submission)

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "using", "exactly", "t", "2-digit terms", "."], cfg)
        assert constraint.is_satisfied(submission)

    def verify_reduces_recursively_constraint(self) -> None:
        class ArrayReducesConstraint(ReducesRecursivelyConstraint):
            def get_unhandled_scenario(self, submission: DPStudentSubmission) -> str:
                return "if we decide to make the last term 2 digits, then we would need to call a subproblem that analyzes the subarray A[1..n-2]"

        constraint = ArrayReducesConstraint("SUBARRAY")

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[1..n]", "under the constraint that", "A[1]", "is part of a", "j-digit", "term", "."], cfg)
        assert not constraint.is_satisfied(submission)
        assert constraint.get_feedback(submission) == "Make sure that your subproblem can be reduced to smaller instances of itself. For example, if we decide to make the last term 2 digits, then we would need to call a subproblem that analyzes the subarray A[1..n-2], but your subproblem definition does not allow us to do that."

        # Check that it still works if the SUBARRAY field is missing entirely
        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained",
             "under the constraint that", "A[1]", "is part of a", "j-digit", "term", "."], cfg)
        assert not constraint.is_satisfied(submission)
        assert constraint.get_feedback(submission) == "Make sure that your subproblem can be reduced to smaller instances of itself. For example, if we decide to make the last term 2 digits, then we would need to call a subproblem that analyzes the subarray A[1..n-2], but your subproblem definition does not allow us to do that."

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "using", "at most", "t", "2-digit terms", "."], cfg)
        assert constraint.is_satisfied(submission)

    def verify_no_irrelevant_restrictions_constraint(self) -> None:
        constraint = NoIrrelevantRestrictions("FIRST_OR_LAST_TERM_RESTRICTION")

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "under the constraint that", "A[1]", "is part of a", "j-digit", "term", "."], cfg)
        assert not constraint.is_satisfied(submission)

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "using", "at most", "t", "2-digit terms", "."], cfg)
        assert constraint.is_satisfied(submission)

    def verify_no_double_ended_parameterization_constraint(self) -> None:
        constraint = NoDoubleEndedParameterization()

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..j]", "under the constraint that", "A[1]", "is part of a", "j-digit", "term", "."], cfg)
        assert not constraint.is_satisfied(submission)

        submission = DPStudentSubmission(
            ["define", "DP(i,j)", "to be the", "maximum", "sum", "that can be obtained", "from",
             "A[i..n]", "using", "at most", "t", "2-digit terms", "."], cfg)
        assert constraint.is_satisfied(submission)


class VerifyMiscellaneousUtils:
    def verify_concat_into_production_rule(self) -> None:
        assert concat_into_production_rule(["DP", "MaxSum"], ["(i)", "(i,j)"]) == \
            '"DP(i)" | "DP(i,j)" | "MaxSum(i)" | "MaxSum(i,j)"'
    @pytest.mark.parametrize(
        "input,expected",
        [(["i"], "i"),
         (["i", "j"], "i and j"),
         (["i", "j", "k"], "i, j, and k"),
         (["b", "a", "c"], "b, a, and c")]
    )
    def verify_list_to_english(self, input: List[str], expected: str) -> None:
        assert list_to_english(input) == expected
