type CFG = {
    start: string;
    productions: Production[];
};

type Production = {
    lhs: string;
    rhs: RhsSymbol[];
};

type RhsSymbol = {
    text: string;
    isTerminal: boolean;
};

type PdaConfig = {
    stack: RhsSymbol[];
    remainingInput: string[]; // list in reverse order
};

function get_possible_next_tokens(input: string[], cfg: CFG): Set<string> {
    const possible_next_tokens: Set<string> = new Set();

    const configs_to_explore: PdaConfig[] = [{
        stack: [{ text: cfg.start, isTerminal: false }],
        remainingInput: input.reverse()
    }];

    while (configs_to_explore.length > 0) {
        const curr_config = configs_to_explore.pop();

        if (curr_config.stack.length === 0) {
            continue; // stack is empty so we can't get a next token from this thread
        }

        const curr_symbol = curr_config.stack.pop();

        if (curr_symbol.isTerminal) {
            if (curr_config.remainingInput.length === 0) {
                possible_next_tokens.add(curr_symbol.text);

            } else {
                const next_token = curr_config.remainingInput.pop();
                if (curr_symbol.text === next_token) {
                    configs_to_explore.push(curr_config);
                }
            }

        } else { // nonterminal, add all of its production rules
            cfg.productions
                .filter(prod => prod.lhs === curr_symbol.text)
                .forEach(prod => configs_to_explore.push({
                    stack: curr_config.stack.concat(prod.rhs.reverse()),
                    remainingInput: curr_config.remainingInput.slice(),
                }));
        }
    }

    return possible_next_tokens;
}

const cfg: CFG = { "start": "START", "productions": [{ "lhs": "START", "rhs": [{ "text": "Define", "isTerminal": true }, { "text": "FUNCTION", "isTerminal": false }, { "text": "to be", "isTerminal": true }, { "text": "the", "isTerminal": true }, { "text": "EXTREMAL_MODIFIER", "isTerminal": false }, { "text": "QUANTITY", "isTerminal": false }, { "text": "PREPOSITIONAL_PHRASE", "isTerminal": false }, { "text": "CONSTRAINT_CLAUSE", "isTerminal": false }, { "text": ".", "isTerminal": true }] }, { "lhs": "FUNCTION", "rhs": [{ "text": "MinCost(i,j)", "isTerminal": true }] }, { "lhs": "FUNCTION", "rhs": [{ "text": "MinCost(i)", "isTerminal": true }] }, { "lhs": "FUNCTION", "rhs": [{ "text": "DP(i,j)", "isTerminal": true }] }, { "lhs": "FUNCTION", "rhs": [{ "text": "DP(i)", "isTerminal": true }] }, { "lhs": "FUNCTION", "rhs": [{ "text": "the subproblem", "isTerminal": true }] }, { "lhs": "FUNCTION", "rhs": [{ "text": "etc.......", "isTerminal": true }] }, { "lhs": "EXTREMAL_MODIFIER", "rhs": [{ "text": "minimum possible", "isTerminal": true }] }, { "lhs": "EXTREMAL_MODIFIER", "rhs": [{ "text": "maximum possible", "isTerminal": true }] }, { "lhs": "EXTREMAL_MODIFIER", "rhs": [] }, { "lhs": "QUANTITY", "rhs": [{ "text": "answer", "isTerminal": true }] }, { "lhs": "QUANTITY", "rhs": [{ "text": "value", "isTerminal": true }] }, { "lhs": "QUANTITY", "rhs": [{ "text": "cost", "isTerminal": true }] }, { "lhs": "QUANTITY", "rhs": [{ "text": "number of hotels used", "isTerminal": true }] }, { "lhs": "QUANTITY", "rhs": [{ "text": "number of coupons used", "isTerminal": true }] }, { "lhs": "PREPOSITIONAL_PHRASE", "rhs": [{ "text": "PREPOSITION", "isTerminal": false }, { "text": "PREPOSITION_OBJECT", "isTerminal": false }] }, { "lhs": "PREPOSITION", "rhs": [{ "text": "of", "isTerminal": true }] }, { "lhs": "PREPOSITION", "rhs": [{ "text": "for", "isTerminal": true }] }, { "lhs": "PREPOSITION", "rhs": [{ "text": "in", "isTerminal": true }] }, { "lhs": "PREPOSITION", "rhs": [{ "text": "while", "isTerminal": true }] }, { "lhs": "PREPOSITION_OBJECT", "rhs": [{ "text": "i", "isTerminal": true }] }, { "lhs": "PREPOSITION_OBJECT", "rhs": [{ "text": "i and j", "isTerminal": true }] }, { "lhs": "PREPOSITION_OBJECT", "rhs": [{ "text": "traveling", "isTerminal": true }, { "text": "from", "isTerminal": true }, { "text": "LOCATION", "isTerminal": false }, { "text": "to", "isTerminal": true }, { "text": "LOCATION", "isTerminal": false }] }, { "lhs": "LOCATION", "rhs": [{ "text": "Hotel 1", "isTerminal": true }] }, { "lhs": "LOCATION", "rhs": [{ "text": "Hotel n", "isTerminal": true }] }, { "lhs": "LOCATION", "rhs": [{ "text": "Hotel i", "isTerminal": true }] }, { "lhs": "LOCATION", "rhs": [{ "text": "Hotel j", "isTerminal": true }] }, { "lhs": "LOCATION", "rhs": [{ "text": "Hotel k", "isTerminal": true }] }, { "lhs": "LOCATION", "rhs": [{ "text": "the current location", "isTerminal": true }] }, { "lhs": "CONSTRAINT_CLAUSE", "rhs": [{ "text": ",", "isTerminal": true }, { "text": "under the constraint that", "isTerminal": true }, { "text": "CONSTRAINT_STATEMENT", "isTerminal": false }] }, { "lhs": "CONSTRAINT_CLAUSE", "rhs": [] }, { "lhs": "CONSTRAINT_STATEMENT", "rhs": [{ "text": "the", "isTerminal": true }, { "text": "QUANTITY", "isTerminal": false }, { "text": "is", "isTerminal": true }, { "text": "COMPARISON_OPERATOR", "isTerminal": false }, { "text": "CONSTRAINT_RHS", "isTerminal": false }] }, { "lhs": "COMPARISON_OPERATOR", "rhs": [{ "text": "at least", "isTerminal": true }] }, { "lhs": "COMPARISON_OPERATOR", "rhs": [{ "text": "at most", "isTerminal": true }] }, { "lhs": "COMPARISON_OPERATOR", "rhs": [{ "text": "exactly", "isTerminal": true }] }, { "lhs": "CONSTRAINT_RHS", "rhs": [{ "text": "the number of coupons we have remaining", "isTerminal": true }] }, { "lhs": "CONSTRAINT_RHS", "rhs": [{ "text": "0", "isTerminal": true }] }, { "lhs": "CONSTRAINT_RHS", "rhs": [{ "text": "1", "isTerminal": true }] }, { "lhs": "CONSTRAINT_RHS", "rhs": [{ "text": "i", "isTerminal": true }] }, { "lhs": "CONSTRAINT_RHS", "rhs": [{ "text": "j", "isTerminal": true }] }, { "lhs": "CONSTRAINT_RHS", "rhs": [{ "text": "k", "isTerminal": true }] }, { "lhs": "CONSTRAINT_RHS", "rhs": [{ "text": "n", "isTerminal": true }] }] };

const input = ["Define", "MinCost(i,j)", "to be", "the"];

console.log(get_possible_next_tokens(input, cfg));
