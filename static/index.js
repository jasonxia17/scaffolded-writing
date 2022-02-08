const entered_tokens = [];

function updateNextTokenList() {
    const next_token_list = $('#next-token-list');
    const no_more_tokens_message = $('#no-more-tokens-message');

    next_token_list.empty();
    no_more_tokens_message.empty();

    const possible_next_tokens = getPossibleNextTokens(entered_tokens, cfg);

    for (const token of possible_next_tokens) {
    $('<span/>')
        .addClass('badge badge-dark m-2')
        .css('cursor', 'default')
        .text(token)
        .appendTo(next_token_list);
    }

    if (possible_next_tokens.size === 0) {
    no_more_tokens_message.text('You have completed your sentence. No more tokens can be appended.');
    $('#submit').prop('disabled', false);
    } else {
    $('#submit').prop('disabled', true);
    }
}

updateNextTokenList();

function handleTokenEnteredOrDeleted() {
    $('#sentence').text(entered_tokens.join(' ').replaceAll(' ,', ',').replaceAll(' .', '.'));
    updateNextTokenList();
}

// need to do this because jquery doesn't support repeat
document.getElementById('next-token-input').addEventListener("keydown", e => {
    if (e.key === "Enter") {
    e.preventDefault();

    const processed_input = e.target.value.trim()
    if (getPossibleNextTokens(entered_tokens, cfg).has(processed_input)) {
        entered_tokens.push(processed_input);
        e.target.value = '';
        handleTokenEnteredOrDeleted();
    }

    } else if (e.key === "Backspace" && e.target.value.length === 0 && !e.repeat) {
    entered_tokens.pop();
    handleTokenEnteredOrDeleted();
    }
});

$('#submit').click(async e => {
    $('#feedback').text('');
    $('.spinner-border').show();

    const response = await fetch('/submit', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(entered_tokens)
    });

    const feedback = await response.text();

    setTimeout(() => {
    $('#feedback').text(feedback);
    $('.spinner-border').hide();
    }, 1500)
});
