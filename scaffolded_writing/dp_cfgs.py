from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.dp_utils import concat_into_production_rule

PARTITION_SUM_CFG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

    FUNCTION_DECLARATION -> "the subproblem" | {concat_into_production_rule(
        ["DP", "Memo", "MinSum", "MaxSum", "MinTerms", "MaxTerms"],
        ["(i)", "(i,j)"]
    )}

    FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "that can be obtained" SITUATION

    EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
    OUTPUT_NOUN -> "answer" | "number of terms" | "sum"
    SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION ADDITIONAL_RESTRICTION

    MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

    SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
    SUBARRAY -> "the rest of the array" | "A[1..n]" | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
    PREFIX_SUBPROBLEM -> "A[1..i]"
    SUFFIX_SUBPROBLEM -> "A[i..n]"
    DOUBLE_ENDED_SUBPROBLEM -> "A[i..j]"

    ADDITIONAL_RESTRICTION -> EPSILON | NUM_TWO_DIGIT_TERMS_RESTRICTION | FIRST_OR_LAST_TERM_RESTRICTION \
                            | NUM_TWO_DIGIT_TERMS_RESTRICTION "and" FIRST_OR_LAST_TERM_RESTRICTION

    NUM_TWO_DIGIT_TERMS_RESTRICTION -> "using" COMPARISON_OPERATOR COMPARISON_RHS "2-digit terms"
    COMPARISON_OPERATOR -> "at least" | VIABLE_COMPARISON_OPERATOR
    VIABLE_COMPARISON_OPERATOR -> "at most" | "exactly"
    COMPARISON_RHS -> "t" | "i" | "j"

    FIRST_OR_LAST_TERM_RESTRICTION -> "under the constraint that" RESTRICTED_TERM_INDEX "is part of a" TERM_LENGTH "term"
    RESTRICTED_TERM_INDEX -> "A[1]" | "A[n]" | "A[i]"
    TERM_LENGTH -> "1-digit" | "2-digit" | "3-digit" | "i-digit" | "j-digit"

    EPSILON ->
""")

GRASSLEARN_CFG =  ScaffoldedWritingCFG.fromstring(f"""
    START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

    FUNCTION_DECLARATION -> "the subproblem" | {concat_into_production_rule(
        ["Memo", "MaxPoints", "MinMinutes", "Streak", "Questions"],
        ["(i)", "(i,j)", "(i,j,k)"]
    )}

    FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "needed" SITUATION

    EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
    OUTPUT_NOUN -> "answer" | "number of questions" | "number of points" | "number of minutes" | "streak"

    SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING \
               | NUM_POINTS_OR_QUESTIONS_RESTRICTION SUBARRAY_RESTRICTION STREAK_RESTRICTION

    MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j" | "for i, j, and k"

    NUM_POINTS_OR_QUESTIONS_RESTRICTION -> EPSILON | NUM_POINTS_RESTRICTION | NUM_QUESTIONS_RESTRICTION
    NUM_POINTS_RESTRICTION -> "to earn" COMPARISON_OPERATOR NUM_POINTS "points"
    NUM_QUESTIONS_RESTRICTION -> "to correctly answer" COMPARISON_OPERATOR NUM_POINTS "questions"

    COMPARISON_OPERATOR -> "at most" | VIABLE_COMPARISON_OPERATOR
    VIABLE_COMPARISON_OPERATOR -> "at least" | "exactly"
    NUM_POINTS -> "p" | "i" | "j" | "k"

    SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
    SUBARRAY -> "the rest of the questions" | "Questions 1 through n" \
              | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
    PREFIX_SUBPROBLEM -> "Questions 1 through i"
    SUFFIX_SUBPROBLEM -> "Questions i through n"
    DOUBLE_ENDED_SUBPROBLEM -> "Questions i through j"

    STREAK_RESTRICTION -> EPSILON | STARTING_OR_ENDING "with a streak of length" STREAK_LENGTH
    STARTING_OR_ENDING -> "starting" | "ending"
    STREAK_LENGTH -> "i" | "j" | "k"

    EPSILON ->
""")

MAX_PROFIT_CFG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "define" FUNCTION_DECLARATION "to be the" FUNCTION_OUTPUT "."

    FUNCTION_DECLARATION -> "the subproblem" | {concat_into_production_rule(
        ["DP", "Memo", "MaxProfit"],
        ["(i)", "(i,j)"]
    )}

    FUNCTION_OUTPUT -> EXTREMAL_ADJ OUTPUT_NOUN "that can be obtained" SITUATION

    EXTREMAL_ADJ -> EPSILON | "minimum" | "maximum"
    OUTPUT_NOUN -> "answer" | "profit"
    SITUATION -> MENTION_PARAMS_WITHOUT_EXPLAINING | SUBARRAY_RESTRICTION \
               | NUM_TRIALS_RESTRICTION SUBARRAY_RESTRICTION

    MENTION_PARAMS_WITHOUT_EXPLAINING -> "for i" | "for i and j"

    SUBARRAY_RESTRICTION -> EPSILON | "from" SUBARRAY
    SUBARRAY -> "the rest of the trials" | "Trials 1 through n" \
              | PREFIX_SUBPROBLEM | SUFFIX_SUBPROBLEM | DOUBLE_ENDED_SUBPROBLEM
    PREFIX_SUBPROBLEM -> "Trials 1 through i"
    SUFFIX_SUBPROBLEM -> "Trials i through n"
    DOUBLE_ENDED_SUBPROBLEM -> "Trials i through j"

    NUM_TRIALS_RESTRICTION -> "by accepting" COMPARISON_OPERATOR COMPARISON_RHS "trials"
    COMPARISON_OPERATOR -> "at least" | "at most" | "exactly"
    COMPARISON_RHS -> "i" | "j"

    EPSILON ->
""")
