from typing import Dict, Any
from scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
import scaffolded_writing.dp_utils as sw_du

from scaffolded_writing.dp_cfgs import PARTITION_SUM_CFG
from shared_utils import set_weighted_score_data

class ArrayReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        return "if we decide to place a plus sign after the first digit, then we would need to compute the maximum sum that can be obtained from A[2..n]"


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
    grader.add_constraint(ArrayReducesConstraint("SUBARRAY"), 0.6)
    grader.add_constraint(sw_du.NoIrrelevantRestrictions("NUM_TWO_DIGIT_TERMS_RESTRICTION", "FIRST_OR_LAST_TERM_RESTRICTION"), 0.7)
    grader.add_constraint(sw_du.NoDoubleEndedParameterization())

    grader.grade_question(data, "subproblem_definition")
    set_weighted_score_data(data)

statement = """
<p>You are given a sequence of digits $A[1..n]$ where each digit is between 1 and 9 (inclusive). You are asked to insert $+$ signs in between the digits to partition them into terms which will be added together. The length of each term in the summation must be either 1 or 2 digits.</p>
<p>What is the maximum sum that can be achieved under these constraints?</p>

<h4>Example</h4>
If  $A = 1912$, then the maximum sum that can be achieved is $1+91+2=94$.
"""
