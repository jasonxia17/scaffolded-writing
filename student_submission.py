from collections import defaultdict
from typing import Optional

from nltk.grammar import CFG, is_terminal
from nltk.parse import RecursiveDescentParser
from nltk.tree import Tree

class StudentSubmission():
    def __init__(self, token_list: list[str], cfg: CFG):
        self.token_list: list[str] = token_list

        parse_tree: Optional[Tree] = RecursiveDescentParser(cfg).parse_one(token_list)
        if parse_tree is None:
            raise ValueError("Student submission could not be parsed by the CFG.")

        # keys = nonterminals that have exactly one child, which is also a leaf
        # corresponding value = the terminal at that leaf
        self.nonterminal_values: dict[str, str] = {
            subtree.label(): subtree.leaves()[0]
            for subtree in parse_tree.subtrees()
            if subtree.height() == 2 and len(subtree.leaves()) == 1
        }

        # the set of ALL possible singleton terminals that could be produced by a given nonterminal
        # based on the CFG's rules
        self.nonterminal_possibilities: dict[str, set[str]] = defaultdict(set)

        for prod in cfg.productions():
            if len(prod.rhs()) == 1 and is_terminal(prod.rhs()[0]):
                self.nonterminal_possibilities[prod.lhs().symbol()].add(prod.rhs()[0])


    def check_nonterminal(self, nonterminal: str, terminal: Optional[str]) -> bool:
        """
        Returns True if nonterminal produces terminal in the parse tree of the student's submission,
        False otherwise.

        Error checking is performed to guard against typos and to ensure that the grading code remains
        consistent with the code for defining the CFG.
        """
        assert nonterminal in self.nonterminal_possibilities
        assert terminal in self.nonterminal_possibilities[nonterminal]
        return self.nonterminal_values.get(nonterminal) == terminal

sentence = ["Define", "MinCost(i,j)", "to be", "the", "minimum possible", "cost", "of", "traveling",
    "from", "Hotel i", "to", "Hotel n", ",", "under the constraint that", "the", "number of coupons used", "is",
    "at most", "j", "."]

from cfg import cfg
print(StudentSubmission(sentence, cfg).check_nonterminal("OUTPUT_QUANTITY", "cost"))
