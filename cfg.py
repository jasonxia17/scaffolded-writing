from nltk.grammar import CFG, is_nonterminal, is_terminal

cfg = CFG.fromstring("""
    START -> "Define" FUNCTION "to be" "the" EXTREMAL_MODIFIER OUTPUT_QUANTITY PREPOSITIONAL_PHRASE CONSTRAINT_CLAUSE "."
    FUNCTION -> "MinCost(i,j)" | "MinCost(i)" | "DP(i,j)" | "DP(i)" | "the subproblem" | "etc......."
    EXTREMAL_MODIFIER -> "minimum possible" | "maximum possible" |
    OUTPUT_QUANTITY -> "answer" | "value" | "cost" | "number of hotels used" | "number of coupons used"
    PREPOSITIONAL_PHRASE -> PREPOSITION PREPOSITION_OBJECT
    PREPOSITION -> "of" | "for" | "in" | "while"
    PREPOSITION_OBJECT -> "i" | "i and j" | "traveling" "from" TRAVEL_ORIGIN "to" TRAVEL_DESTINATION
    TRAVEL_ORIGIN -> "Hotel 1" | "Hotel i" | "Hotel j" | "Hotel k" | "the current location"
    TRAVEL_DESTINATION -> "Hotel n" | "Hotel i" | "Hotel j" | "Hotel k" | "the current location"
    CONSTRAINT_CLAUSE -> "," "under the constraint that" CONSTRAINT_STATEMENT |
    CONSTRAINT_STATEMENT -> "the" CONSTRAINT_QUANTITY "is" COMPARISON_OPERATOR CONSTRAINT_RHS
    CONSTRAINT_QUANTITY -> "cost" | "number of hotels used" | "number of coupons used"
    COMPARISON_OPERATOR -> "at least" | "at most" | "exactly"
    CONSTRAINT_RHS -> "the number of coupons we have remaining" | "0" | "1" | "i" | "j" | "k" | "n"
""")

# check that no nonterminals appear multiple times (that would break the current design of the grader)
rhs_nonterminals = [symbol for prod in cfg.productions() for symbol in prod.rhs() if is_nonterminal(symbol)]
assert len(rhs_nonterminals) == len(set(rhs_nonterminals))

# Check that all nonterminals appear on both lhs and rhs (except START, which should only appear on the lhs)
lhs_nonterminals = {prod.lhs() for prod in cfg.productions()}
assert lhs_nonterminals - {cfg.start()} == set(rhs_nonterminals)

cfg_as_json = {
    "start": cfg.start().symbol(),
    "productions": [
        {
            "lhs": prod.lhs().symbol(),
            "rhs": [{"text": str(symbol), "isTerminal": is_terminal(symbol)} for symbol in prod.rhs()]
        }
        for prod in cfg.productions()
    ]
}
