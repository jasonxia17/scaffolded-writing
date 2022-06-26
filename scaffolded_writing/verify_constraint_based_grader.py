import pytest
import scaffolded_writing.dp_utils as sw_du
from scaffolded_writing.dp_cfgs import PARTITION_SUM_CFG as cfg
from scaffolded_writing.constraint_based_grader import IncrementalConstraintGrader
from shared_utils import get_partial_score
from typing import List, Dict, Any


def verify_incremental_constraint_grader_exception_submission_type() -> None:
    # Check that grader must be given a valid student submission type
    with pytest.raises(TypeError, match='is not a subclass of StudentSubmission'):
        grader = IncrementalConstraintGrader(sw_du.CanComputeFinalAnswer, cfg)  # type: ignore

        grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0)  # type: ignore


def verify_incremental_constraint_grader_exception_credit_range() -> None:
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, cfg)

    # Check that partial credit must be in the range (0, 1]
    with pytest.raises(ValueError, match=r'partial credit is not in \(0,1]'):
        grader.add_constraint(sw_du.DeclareFunctionConstraint(), -1)

    with pytest.raises(ValueError, match=r'partial credit is not in \(0,1]'):
        grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0)

    with pytest.raises(ValueError, match=r'partial credit is not in \(0,1]'):
        grader.add_constraint(sw_du.DeclareFunctionConstraint(), 2)


def verify_incremental_constraint_grader_exception_constraint_order() -> None:
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, cfg)

    grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.5)

    # Check that partial scores must be increasing for this grader type
    with pytest.raises(ValueError, match='value not increasing'):
        grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.5)

    with pytest.raises(ValueError, match='value not increasing'):
        grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.3)


def verify_incremental_constraint_grader_exception_partial_scores() -> None:
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, cfg)

    # Data dict for grader tests
    data: Dict[str, Any] = dict()

    # Check that grader is called with a nonzero number of constraints
    with pytest.raises(ValueError, match='No constraints set'):
        grader.grade_question(data, 'name')

    grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.5)

    # Check that last partial score given to grader grants full credit
    with pytest.raises(ValueError, match="doesn't grant full credit"):
        grader.grade_question(data, 'name')


@pytest.mark.parametrize(
    "student_tokens, expected_grade",
    [(["define", "the subproblem", "to be the", "maximum", "sum", "that can be obtained", "."], 0.0),
     (["define", "DP(i)", "to be the", "answer", "that can be obtained", "."], 0.05),
     (["define", "DP(i)", "to be the", "maximum", "sum", "that can be obtained", "."], 0.1),
     (["define", "MaxSum(i)", "to be the", "maximum", "sum", "that can be obtained", "."], 0.15),
     (["define", "MaxSum(i)", "to be the", "maximum", "sum", "that can be obtained", "from",
      "A[i..n]", "using", "at most", "t", "2-digit terms", "."], 1.0)
     ]
)
def verify_incremental_constraint_grader(student_tokens: List[str],
                                         expected_grade: float) -> None:

    # Configure grader
    grader = IncrementalConstraintGrader(sw_du.DPStudentSubmission, cfg)

    grader.add_constraint(sw_du.DeclareFunctionConstraint(), 0.05)
    grader.add_constraint(sw_du.CorrectOutputNounAndExtremalAdj("sum", "maximum"), 0.1)
    grader.add_constraint(sw_du.DescriptiveFunctionName("MaxSum"), 0.15)
    grader.add_constraint(sw_du.ExplainParamsConstraint(variables_in_problem=["n", "t"]))

    # Set up data dictionary
    data: Dict[str, Dict[str, Any]] = dict()
    question_name = 'name'

    data['partial_scores'] = dict()
    data['submitted_answers'] = {question_name: student_tokens}
    data['feedback'] = dict()

    # Grade question
    grader.grade_question(data, question_name)
    assert get_partial_score(data, question_name) == expected_grade

    # Assert we get feedback if we didn't get full credit
    if expected_grade < 1.0:
        assert data['feedback'][question_name]
