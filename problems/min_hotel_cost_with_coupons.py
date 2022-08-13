from typing import Dict, Any
from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
import scaffolded_writing.dp_utils as sw_du

from shared_utils import set_weighted_score_data

MIN_HOTEL_COST_CFG = ScaffoldedWritingCFG.fromstring(f"""
SENTENCE -> "Define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

FUNCTION_DECLARATION -> "the subproblem" | "DP(i)" | "DP(i,j)" | "MinCost(i)" | "MinCost(i,j)"

FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN SITUATION

EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"

OUTPUT_NOUN -> "answer" | "cost" | "hotels" | "coupons"
NOUN -> "answer" | "cost" | "hotels" | "coupons"

SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | "of" SUBARRAY_RESTRICTION ADDITIONAL_RESTRICTION

MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

SUBARRAY_RESTRICTION -> "traveling from" ORIGIN "to" DESTINATION

ORIGIN -> "the current location" | VIABLE_ORIGIN | "Hotel n" | "Hotel k"
VIABLE_ORIGIN -> "Hotel 1" | "Hotel i" | "Hotel j"

DESTINATION -> "the current location" | "Hotel 1" | VIABLE_DESTINATION | "Hotel k"
VIABLE_DESTINATION -> "Hotel i" | "Hotel j" | "Hotel n"

ADDITIONAL_RESTRICTION -> EPSILON | "using" COMPARISON_OPERATOR COMPARISON_RHS NOUN

COMPARISON_OPERATOR -> "at least" | VIABLE_COMPARISON_OPERATOR
VIABLE_COMPARISON_OPERATOR -> "at most" | "exactly"

COMPARISON_RHS -> "0" | "1" | "i" | "j" | "k" | "n"

EPSILON ->
""")

class ArrayReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        return "if we decide to travel to Hotel 2 on the first day, then we would need to compute the minimum cost of traveling from Hotel 2 to Hotel n"


class NumTwoDigitTermsReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        return f"if we have k coupons and decide to user a coupon, then we would need to enforce that the rest of the trip uses at most <b><em>(k-1)</em></b> coupons"


def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = MIN_HOTEL_COST_CFG.to_json_string()


def grade(data: Dict[str, Any]) -> None:
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, MIN_HOTEL_COST_CFG)

    grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.05)
    grader.add_constraint(sw_du.CorrectOutputNounAndExtremalAdj("cost", "minimum"), 0.1)
    grader.add_constraint(sw_du.DescriptiveFunctionName("MinCost"), 0.15)
    grader.add_constraint(sw_du.ExplainParamsConstraint(variables_in_problem=["n", "k"]), 0.25)

    grader.add_constraint(sw_du.CanComputeFinalAnswer(
        ["SUBARRAY_RESTRICTION", "ORIGIN", "VIABLE_ORIGIN"],
        "we start at Hotel 1"
    ), 0.3)
    grader.add_constraint(sw_du.CanComputeFinalAnswer(
        ["SUBARRAY_RESTRICTION", "DESTINATION", "VIABLE_DESTINATION"],
        "we end at Hotel n"
    ), 0.4)

    grader.add_constraint(sw_du.CanComputeFinalAnswer(
        ["ADDITIONAL_RESTRICTION", "NOUN", "coupons"],
        "at most k coupons are used"
    ), 0.5)
    grader.add_constraint(sw_du.CanComputeFinalAnswer(
        ["ADDITIONAL_RESTRICTION", "COMPARISON_OPERATOR", "VIABLE_COMPARISON_OPERATOR"],
        "at most k coupons are used"
    ), 0.6)

    grader.add_constraint(sw_du.DecoupledParametersConstraint(
        ORIGIN="starting location",
        DESTINATION="ending location",
        COMPARISON_RHS="number of coupons",
    ), 0.7)

    grader.add_constraint(ArrayReducesConstraint("SUBARRAY_RESTRICTION"), 0.8)
    grader.add_constraint(NumTwoDigitTermsReducesConstraint("COMPARISON_RHS"))
    # grader.add_constraint(sw_du.NoDoubleEndedParameterization())
    # TODO: implement check for double ended parameterization (needed for no-coupon version)

    grader.grade_question(data, "subproblem_definition")
    set_weighted_score_data(data)

statement = """
<p>
    You are planning a road trip along a highway with $n$ evenly-spaced hotels. These hotels have varying costs; the costs of staying overnight at each of the hotels are provided in the array $HotelCosts[1..n]$, where $HotelCosts[i]$ is the cost of Hotel $i$. Each day, you can either travel to the next hotel, or you can skip a hotel and travel forward by two hotels. Each night, you must stay at a hotel. Furthermore, you have $k$ coupons that allow you to stay at a hotel for free. Describe a dynamic programming algorithm to determine the minimum possible cost of traveling from Hotel $1$ to Hotel $n$.
</p>
"""
