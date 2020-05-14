function replayFunction(get_absolute_url) {
    get_absolute_url = get_absolute_url.toString().replace(/[ \/ ]/gi, '');
    get_absolute_url = get_absolute_url.replace(/\\\\/gi, "/")
    $.ajax({
        type: "POST",
        url: get_absolute_url,
        data: {
            content: $('#content').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
    });
};







