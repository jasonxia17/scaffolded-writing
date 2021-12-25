import json
from nltk.grammar import CFG, is_nonterminal, is_terminal
from nltk import Tree

cfg = CFG.fromstring("""
    START -> "Define" FUNCTION "to be" "the" EXTREMAL_MODIFIER QUANTITY PREPOSITIONAL_PHRASE CONSTRAINT_CLAUSE "."
    FUNCTION -> "MinCost(i,j)" | "MinCost(i)" | "DP(i,j)" | "DP(i)" | "the subproblem" | "etc......."
    EXTREMAL_MODIFIER -> "minimum possible" | "maximum possible" |
    QUANTITY -> "answer" | "value" | "cost" | "number of hotels used" | "number of coupons used"
    PREPOSITIONAL_PHRASE -> PREPOSITION PREPOSITION_OBJECT
    PREPOSITION -> "of" | "for" | "in" | "while"
    PREPOSITION_OBJECT -> "i" | "i and j" | "traveling" "from" LOCATION "to" LOCATION
    LOCATION -> "Hotel 1" | "Hotel n" | "Hotel i" | "Hotel j" | "Hotel k" | "the current location"
    CONSTRAINT_CLAUSE -> "," "under the constraint that" CONSTRAINT_STATEMENT |
    CONSTRAINT_STATEMENT -> "the" QUANTITY "is" COMPARISON_OPERATOR CONSTRAINT_RHS
    COMPARISON_OPERATOR -> "at least" | "at most" | "exactly"
    CONSTRAINT_RHS -> "the number of coupons we have remaining" | "0" | "1" | "i" | "j" | "k" | "n"
""")

# Check that all nonterminals except START appear on both lhs and rhs at some point
lhs_nonterminals = {prod.lhs() for prod in cfg.productions()}
rhs_nonterminals = {symbol for prod in cfg.productions() for symbol in prod.rhs() if is_nonterminal(symbol)}
assert lhs_nonterminals == rhs_nonterminals | {cfg.start()}, \
    f"symmetric difference: {lhs_nonterminals ^ rhs_nonterminals}"

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

print(json.dumps(cfg_as_json))
