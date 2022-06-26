from abc import ABC, abstractmethod
from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.student_submission import StudentSubmission
from shared_utils import grade_question_parameterized
from typing import Generic, List, Optional, Tuple, TypeVar, Dict, Any, Type

SubmissionT = TypeVar('SubmissionT', bound=StudentSubmission)

class Constraint(ABC, Generic[SubmissionT]):
    @abstractmethod
    def is_satisfied(self, submission: SubmissionT) -> bool: ...

    @abstractmethod
    def get_feedback(self, submission: SubmissionT) -> str: ...


class IncrementalConstraintGrader(Generic[SubmissionT]):
    "Class for incrementally constructing a grader for scaffolded writing questions"
    constraints: List[Tuple[Constraint[SubmissionT], float]]

    def __init__(self, submission_type: Type[SubmissionT], question_cfg: ScaffoldedWritingCFG) -> None:
        if not issubclass(submission_type, StudentSubmission):
            raise TypeError(f"Submission type {submission_type} is not a subclass of StudentSubmission")
        self.submission_type = submission_type
        self.question_cfg = question_cfg
        self.constraints: List[Tuple[Constraint[SubmissionT], float]] = []


    def add_constraint(self, constraint: Constraint[SubmissionT], partial_credit: float = 1.0) -> None:
        "Add constraint to use for grading, granting partial_credit if the constraint is satisfied"
        if not 0.0 < partial_credit <= 1.0:
            raise ValueError(f"The value {partial_credit} given for partial credit is not in (0,1]")
        elif len(self.constraints) > 0 and self.constraints[-1][1] >= partial_credit:
            raise ValueError("New partial credit value not increasing")

        self.constraints.append((constraint, partial_credit))


    def grade_question(self, data: Dict[str, Any], question_name: str) -> None:
        "Grade question_name using the constraints in the given list"
        if len(self.constraints) == 0:
            raise ValueError("No constraints set for this grader")
        elif self.constraints[-1][1] != 1.0:
            raise ValueError("Final constraint in grader doesn't grant full credit")

        def constraint_grader(tokens: List[str]) -> Tuple[float, Optional[str]]:
            submission = self.submission_type(tokens, self.question_cfg)

            prev_score = 0.0
            for (constraint, partial_credit) in self.constraints:
                if not constraint.is_satisfied(submission):
                    return prev_score, constraint.get_feedback(submission)

                prev_score = partial_credit

            return prev_score, None

        grade_question_parameterized(data, question_name, constraint_grader)
