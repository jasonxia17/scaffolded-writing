from typing import Dict, Any
from scaffolded_writing.constraint_based_grader import Constraint, IncrementalConstraintGrader
import scaffolded_writing.dp_utils as sw_du

from scaffolded_writing.dp_cfgs import MAX_PROFIT_CFG
from shared_utils import set_weighted_score_data

class ArrayReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        return "if we decide to take the first trial and skip[0] = 3, then we would need to compute the maximum profit that can be obtained from Trials 5 through n"


class NoPrefixSubproblems(Constraint[sw_du.DPStudentSubmission]):
    def is_satisfied(self, submission: sw_du.DPStudentSubmission) -> bool:
        return not submission.does_path_exist("PREFIX_SUBPROBLEM")

    def get_feedback(self, submission: sw_du.DPStudentSubmission) -> str:
        return "Using prefix subproblems actually doesn't work for this problem, because these prefix subproblems don't reduce recursively. Think about why this is the case and why suffix subproblems don't have the same issue."


def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = MAX_PROFIT_CFG.to_json_string()


def grade(data: Dict[str, Any]) -> None:
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, MAX_PROFIT_CFG)

    grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.05)
    grader.add_constraint(sw_du.CorrectOutputNounAndExtremalAdj("profit", "maximum"), 0.1)
    grader.add_constraint(sw_du.DescriptiveFunctionName("MaxProfit"), 0.15)
    grader.add_constraint(sw_du.ExplainParamsConstraint(variables_in_problem=["n"]), 0.25)
    grader.add_constraint(sw_du.DecoupledParametersConstraint(
            SUBARRAY="the index of a trial",
            COMPARISON_RHS="the number of trials accepted",
        ), 0.3)
    grader.add_constraint(ArrayReducesConstraint("SUBARRAY"), 0.5)
    grader.add_constraint(NoPrefixSubproblems(), 0.6)
    grader.add_constraint(sw_du.NoIrrelevantRestrictions("NUM_TRIALS_RESTRICTION"), 0.7)
    grader.add_constraint(sw_du.NoDoubleEndedParameterization())

    grader.grade_question(data, "subproblem_definition")
    set_weighted_score_data(data)

statement = """
<p>After the Revolutionary War, Alexander Hamilton's biggest rival as a lawyer was Aaron Burr. (Sir!) In fact, the two worked next door to each other. Unlike Hamilton, Burr cannot work non-stop; every trial he tries exhausts him. The bigger the trial, the longer he must rest before he is well enough to take the next trial. (Of course, he is willing to wait for it.) If a trial arrives while Burr is resting, Hamilton snatches it up instead. Burr has been asked to consider a sequence of $n$ upcoming trials. He quickly computes two arrays $profit[1 .. n]$ and $skip[1 .. n]$, where for each index $i$,
<ul>
    <li>$profit[i]$ is the amount of money Burr would make by taking the $i$th trial, and</li>
    <li>$skip[i]$ is the number of consecutive trials Burr must skip if he accepts the $i$th trial. (That is, if Burr accepts the $i$th trial, he cannot accept trials $i + 1$ through $i + skip[i]$.)</li>
</ul>
<p>What is the maximum total profit Burr can secure from these $n$ trials?</p>

<h5>Example</h5>
<p>If $profit = [3, 7, 3, 5, 6, 4]$ and $skip = [2, 0, 2, 3, 1, 2]$, then Burr should take trial 2, rest for no trials, take trial 3, rest for 2 trials, then finally take trial 6. The total profit would be $7 + 3 + 4 = 14$.</p>
"""
