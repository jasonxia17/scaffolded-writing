// contains logic specific to standalone website (not shared by PL)

entered_tokens = [];
setUpScaffoldedWritingQuestion("", entered_tokens, cfg);

$('.question-grade').click(async e => {
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

    $('#feedback').text(feedback);
    renderMathInElement(document.getElementById('feedback'), katex_macros);
    $('#feedback-modal').modal('show');
});
