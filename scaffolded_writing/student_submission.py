from nltk.parse import RecursiveDescentParser
from nltk.tree import Tree
from typing import List, Union

from scaffolded_writing.cfg import ScaffoldedWritingCFG

# Note: the ValueError (PARSE_ERROR) is meant to be feedback for the student
# All other exceptions are intended to prevent developer mistakes during question development
PARSE_ERROR = ValueError(
    "Your submission could not be parsed. This error may have been caused by submitting an incomplete response."
)

class AmbiguousParseException(Exception):
    """
    Raised if the CFG is ambiguous and there are multiple ways to parse the student submission.
    """
    pass

class PathCanNeverExistWarning(Exception):
    """
    To guard against potential mistakes (e.g. typos, updating the CFG without updating the grading code),
    this exception is raised if the path specified by the grading code could not *possibly* exist
    in *any* parse tree produced by the CFG. In other words, if a check would always return False on every
    possible student submission, then the person writing the check probably made a mistake, so we should
    raise an alarm about that.
    """
    pass

class StudentSubmission():
    def __init__(self, token_list: List[str], cfg: ScaffoldedWritingCFG):
        self.token_list = token_list
        self.cfg = cfg

        try:
            possible_parse_trees = RecursiveDescentParser(cfg).parse_all(token_list)
        except ValueError:
            raise PARSE_ERROR

        if len(possible_parse_trees) == 0:
            raise PARSE_ERROR
        elif len(possible_parse_trees) > 1:
            raise AmbiguousParseException

        self.parse_tree = possible_parse_trees[0]

    def does_path_exist(self, *path: str) -> bool:
        """
        If we treat the parse tree as a directed graph where each node is labeled with the string that
        represents the terminal/nonterminal at that node, then this function returns True iff there
        exists a path in the tree whose labels exactly match the specified labels.
        """
        assert len(path) > 0

        if not self.cfg.can_produce_path(*path):
            raise PathCanNeverExistWarning

        # Handle edge case where path is just a single terminal
        if len(path) == 1 and path[0] in self.token_list:
            return True

        def does_path_exist_starting_from_node(path: List[str], node: Union[Tree, str]) -> bool:
            node_label = node if isinstance(node, str) else node.label()

            if path[0] != node_label:
                return False

            if len(path) == 1:
                return True

            # len(path) >= 2, so the current node cannot be a terminal
            if isinstance(node, str):
                return False

            # figure out if any of the children can generate the rest of the path
            return any(does_path_exist_starting_from_node(path[1:], child) for child in node)

        return any(
            does_path_exist_starting_from_node(list(path), node)
            for node in self.parse_tree.subtrees()
        )
