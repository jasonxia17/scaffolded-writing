import pytest

from typing import List

from scaffolded_writing.student_submission import StudentSubmission, PathCanNeverExistWarning, AmbiguousParseException
from scaffolded_writing.cfg import ScaffoldedWritingCFG

cfg = ScaffoldedWritingCFG.fromstring("""
    SENTENCE -> SUBJECT VERB OBJECT "." | INTERJECTION "!"
    SUBJECT -> NOUN
    NOUN -> "Jason" | "the squirrel"
    VERB -> "ate" | "fought" | "kicked" | "hugged"
    OBJECT -> NOUN | EPSILON
    INTERJECTION -> "Wow" | "Ouch"
    EPSILON ->
""")

ambiguous_cfg = ScaffoldedWritingCFG.fromstring("""
    S -> A A
    A -> "a" | "a" "a"
""")


class VerifyStudentSubmission:
    def verify_no_parse_exception(self) -> None:
        with pytest.raises(ValueError, match="could not be parsed"):
            StudentSubmission(["ate", "Jason", "."], cfg)

        with pytest.raises(ValueError, match="could not be parsed"):
            StudentSubmission(["Json", "ate", "."], cfg)

    def verify_multiple_parses_exception(self) -> None:
        with pytest.raises(AmbiguousParseException):
            StudentSubmission(["a", "a", "a"], ambiguous_cfg)

    def verify_does_path_exist(self) -> None:
        submission = StudentSubmission(["Jason", "fought", "the squirrel", "."], cfg)

        # Single terminal
        assert submission.does_path_exist("Jason")
        assert submission.does_path_exist("fought")
        assert submission.does_path_exist("the squirrel")
        assert submission.does_path_exist(".")

        assert not submission.does_path_exist("ate")
        assert not submission.does_path_exist("!")

        # Single non-terminal
        assert submission.does_path_exist("SENTENCE")
        assert submission.does_path_exist("SUBJECT")
        assert submission.does_path_exist("VERB")
        assert submission.does_path_exist("OBJECT")

        assert not submission.does_path_exist("INTERJECTION")

        # Paths of length 2 ending on a terminal
        assert submission.does_path_exist("NOUN", "Jason")
        assert submission.does_path_exist("VERB", "fought")
        assert submission.does_path_exist("NOUN", "the squirrel")
        assert submission.does_path_exist("SENTENCE", ".")

        assert not submission.does_path_exist("VERB", "kicked")
        assert not submission.does_path_exist("SENTENCE", "!")

        # Paths of length 2 ending on a non-terminal
        assert submission.does_path_exist("SENTENCE", "OBJECT")
        assert submission.does_path_exist("OBJECT", "NOUN")

        assert not submission.does_path_exist("SENTENCE", "INTERJECTION")

        # Longer paths
        assert submission.does_path_exist("SUBJECT", "NOUN", "Jason")
        assert submission.does_path_exist("OBJECT", "NOUN", "the squirrel")

        assert not submission.does_path_exist("OBJECT", "NOUN", "Jason")
        assert not submission.does_path_exist("SUBJECT", "NOUN", "the squirrel")

    @pytest.mark.parametrize(
        "path",
        [
            ["INTERSECTION"],                   # typo in nonterminal
            ["Json"],                           # typo in terminal
            ["SUBJECT", "Jason"],               # missing intermediate node (NOUN)
            ["VERB", "Jason"],                  # terminal that can't be produced
            ["SUBJECT", "VERB"],                # non-terminal that can't be produced
            ["NOUN", "Jason", "SENTENCE"],      # nothing can come after a terminal

            # a longer path where the issue occurs in the middle
            ["SENTENCE", "OBJECT", "NOUN", "VERB", "ate"],
        ]
    )
    def verify_exception_on_checks_that_always_return_false(self, path: List[str]) -> None:
        submission = StudentSubmission(["Wow", "!"], cfg)

        with pytest.raises(PathCanNeverExistWarning):
            submission.does_path_exist(*path)

    def verify_behavior_with_epsilon_productions(self) -> None:
        # OBJECT has a child in this parse tree, so its epsilon production was not used
        submission = StudentSubmission(["Jason", "fought", "the squirrel", "."], cfg)
        assert not submission.does_path_exist("SENTENCE", "OBJECT", "EPSILON")

        # OBJECT has no children in this parse tree, so its epsilon production was used
        submission = StudentSubmission(["Jason", "fought", "."], cfg)
        assert submission.does_path_exist("SENTENCE", "OBJECT", "EPSILON")

        with pytest.raises(PathCanNeverExistWarning):
            # SUBJECT doesn't have an epsilon production, so it is impossible
            # for this path to exist in any parse tree generated by this CFG.
            submission.does_path_exist("SUBJECT", "EPSILON")

        with pytest.raises(PathCanNeverExistWarning):
            # Terminals are only allowed to appear at the end of the path
            submission.does_path_exist("hugged", "EPSILON")
