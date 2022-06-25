// contains logic specific to standalone website (not shared by PL)

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
