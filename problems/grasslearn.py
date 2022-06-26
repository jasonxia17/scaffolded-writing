from typing import Dict, Any
from scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from scaffolded_writing.dp_cfgs import GRASSLEARN_CFG
from shared_utils import set_weighted_score_data
import scaffolded_writing.dp_utils as sw_du

class ArrayReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        return "if we decide to answer the first question incorrectly, then we would need to compute the minimum number of minutes required to earn at least p points from Questions 2 through n"


class NumPointsReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        return "if we decide to answer the first question correctly, then we would need to enforce that we earn at least <b><em>(p-1)</em></b> points from the rest of the questions"


class StreakLengthReducesConstraint(sw_du.ReducesRecursivelyConstraint):
    def is_satisfied(self, submission: sw_du.DPStudentSubmission) -> bool:
        if not super().is_satisfied(submission):
            return False

        if (
            submission.does_path_exist("PREFIX_SUBPROBLEM") and
            submission.does_path_exist("STARTING_OR_ENDING", "starting")
        ):
            return False

        if (
            submission.does_path_exist("SUFFIX_SUBPROBLEM") and
            submission.does_path_exist("STARTING_OR_ENDING", "ending")
        ):
            return False

        return True

    def get_unhandled_scenario(self, submission: sw_du.DPStudentSubmission) -> str:
        if submission.does_path_exist("PREFIX_SUBPROBLEM"):
            return "if we decide to answer the last question correctly, then we need to know the length of the streak that we ended with in order to know how many points we will earn from that question"
        else:
            return "if we decide to answer the first question correctly, then we would need to enforce that we start with a streak of length 1 when analyzing the rest of the questions"


def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = GRASSLEARN_CFG.to_json_string()


def grade(data: Dict[str, Any]) -> None:
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, GRASSLEARN_CFG)

    grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.05)
    grader.add_constraint(sw_du.CorrectOutputNounAndExtremalAdj("number of minutes", "minimum"), 0.1)
    grader.add_constraint(sw_du.DescriptiveFunctionName("MinMinutes"), 0.15)
    grader.add_constraint(sw_du.ExplainParamsConstraint(variables_in_problem=["n", "p"]), 0.25)
    grader.add_constraint(sw_du.DecoupledParametersConstraint(
        SUBARRAY="the index of a question",
        NUM_POINTS="the number of points required",
        STREAK_LENGTH="the streak length",
    ), 0.3)
    grader.add_constraint(sw_du.CanComputeFinalAnswer(
        ["NUM_POINTS_RESTRICTION", "COMPARISON_OPERATOR", "VIABLE_COMPARISON_OPERATOR"],
        "you earn at least p points"
    ), 0.4)
    grader.add_constraint(ArrayReducesConstraint("SUBARRAY"), 0.5)
    grader.add_constraint(NumPointsReducesConstraint("NUM_POINTS"), 0.6)
    grader.add_constraint(StreakLengthReducesConstraint("STREAK_LENGTH"), 0.7)
    grader.add_constraint(sw_du.NoDoubleEndedParameterization())

    grader.grade_question(data, "subproblem_definition")
    set_weighted_score_data(data)

statement = """
<p>For your algorithms class, you have to use an online learning platform called GrassLearn to complete your homework. Your homework consists of $n$ questions, and you have to complete them in order (i.e., you cannot skip a question and go back to it later). GrassLearn keeps track of your <em>streak</em>. Your streak starts at 0 at the beginning of an assignment, it increments by 1 every time you answer a question correctly, and it resets to 0 when you answer a question incorrectly. When you answer a question correctly, you earn $s$ points, where $s$ is the length of your streak after answering that question.</p>

<p>Let $TimeNeeded[1..n]$ be an array of positive integers where $TimeNeeded[i]$ is the number of minutes required to answer Question $i$ correctly. You can assume that you don't spend any time on questions that you answer incorrectly.</p>

<p>In order to get a grade that you're happy with, you want to earn at least $p$ total points on this assignment. What is the minimum number of minutes you need to spend in order to achieve this goal?</p>

<h4>Example</h4>
<p>Consider $TimeNeeded = [20, 10, 5, 100, 2, 1]$.</p>
<ul>
    <li>If $p = 6$, then answering Questions 2, 3, 5, and 6 correctly will earn $1+2+1+2=6$ points, and this will take $10+5+2+1=18$ minutes.</li>
    <li>If $p = 7$, then answering Questions 1, 2, 3, and 6 correctly will earn $1+2+3+1=7$ points, and this will take $20+10+5+1=36$ minutes.</li>
</ul>
"""
