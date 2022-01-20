function getPossibleNextTokens(input, cfg) {
    var possible_next_tokens = new Set();
    var configs_to_explore = [{
            stack: [{ text: cfg.start, isTerminal: false }],
            remainingInput: input.slice().reverse()
        }];
    var _loop_1 = function () {
        var curr_config = configs_to_explore.pop();
        if (curr_config.stack.length === 0) {
            return "continue";
        }
        var curr_symbol = curr_config.stack.pop();
        if (curr_symbol.isTerminal) {
            if (curr_config.remainingInput.length === 0) {
                possible_next_tokens.add(curr_symbol.text);
            }
            else {
                var next_token = curr_config.remainingInput.pop();
                if (curr_symbol.text === next_token) {
                    configs_to_explore.push(curr_config);
                }
            }
        }
        else {
            cfg.productions
                .filter(function (prod) { return prod.lhs === curr_symbol.text; })
                .forEach(function (prod) { return configs_to_explore.push({
                stack: curr_config.stack.concat(prod.rhs.slice().reverse()),
                remainingInput: curr_config.remainingInput.slice()
            }); });
        }
    };
    while (configs_to_explore.length > 0) {
        _loop_1();
    }
    return possible_next_tokens;
}
