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

function getPossibleNextTokens(input: string[], cfg: CFG): Set<string> {
    const possible_next_tokens: Set<string> = new Set();

    const configs_to_explore: PdaConfig[] = [{
        stack: [{ text: cfg.start, isTerminal: false }],
        remainingInput: input.slice().reverse()
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
                    stack: curr_config.stack.concat(prod.rhs.slice().reverse()),
                    remainingInput: curr_config.remainingInput.slice(),
                }));
        }
    }

    return possible_next_tokens;
}
