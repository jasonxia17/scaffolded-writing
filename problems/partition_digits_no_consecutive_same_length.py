from typing import Dict, Any
from scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
import scaffolded_writing.dp_utils as sw_du

from scaffolded_writing.dp_cfgs import PARTITION_SUM_CFG
from shared_utils import set_weighted_score_data

class ArrayReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        return "if we decide to place a plus sign after the first digit, then we would need to compute the maximum sum that can be obtained from A[2..n]"


class TermLengthReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        if submission.does_path_exist("PREFIX_SUBPROBLEM"):
            first_or_last = "last"
            second_or_second_last = "second-to-last"
        else:
            first_or_last = "first"
            second_or_second_last = "second"

        return f"if we decide to group the {first_or_last} two digits into a 2-digit term, then we would need to enforce that the {second_or_second_last} term of the summation is 1 <em>or</em> 3 digits long"


class TermPositionReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        if submission.does_path_exist("PREFIX_SUBPROBLEM"):
            first_or_last = "last"
            restricted_index = "A[n-3]"
        else:
            first_or_last = "first"
            restricted_index = "A[4]"

        return f"if we decide to group the {first_or_last} three digits into a 3-digit term, then we would need to restrict the length of the term that {restricted_index} belongs to"


def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = PARTITION_SUM_CFG.to_json_string()


def grade(data: Dict[str, Any]) -> None:
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, PARTITION_SUM_CFG)

    grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.05)
    grader.add_constraint(sw_du.CorrectOutputNounAndExtremalAdj("sum", "maximum"), 0.1)
    grader.add_constraint(sw_du.DescriptiveFunctionName("MaxSum"), 0.15)
    grader.add_constraint(sw_du.ExplainParamsConstraint(variables_in_problem=["n"]), 0.25)
    grader.add_constraint(sw_du.DecoupledParametersConstraint(
            SUBARRAY="an array index",
            COMPARISON_RHS="the number of 2-digit terms",
            TERM_LENGTH="a term length",
        ), 0.3)
    grader.add_constraint(ArrayReducesConstraint("SUBARRAY"), 0.4)
    grader.add_constraint(TermPositionReducesConstraint("RESTRICTED_TERM_INDEX"), 0.5)
    grader.add_constraint(TermLengthReducesConstraint("TERM_LENGTH"), 0.6)
    grader.add_constraint(sw_du.NoIrrelevantRestrictions("NUM_TWO_DIGIT_TERMS_RESTRICTION"), 0.7)
    grader.add_constraint(sw_du.NoDoubleEndedParameterization())

    grader.grade_question(data, "subproblem_definition")
    set_weighted_score_data(data)

statement = """
<p>You are given a sequence of digits $A[1..n]$ where each digit is between 1 and 9 (inclusive). You are asked to insert $+$ signs in between the digits to partition them into terms which will be added together. The length of each term in the summation must be either 1, 2, or 3 digits. Furthermore, no two consecutive terms in the summation can have the same length.</p>
<p>What is the maximum sum that can be achieved under these constraints?</p>

<h5>Example</h5>
If $A = 9212121921$, then the maximum sum that can be achieved is $921+2+12+1+921=1857$.
<ul>
    <li>Note that $921+212+1+921=2055$ achieves a larger sum, but this is not allowed because there are two consecutive 3-digit terms.</li>
    <li>Similarly, $921+21+21+921=1884$ is not allowed because there are two consecutive 2-digit terms.</li>
    <li>Similarly, $921+21+2+1+921=1866$ is not allowed because there are two consecutive 1-digit terms.</li>
</ul>
"""
