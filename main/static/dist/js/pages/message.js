function replayFunction(get_absolute_url) {
    alert(1)
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

////////////////////////////////


function sentFunction(get_absolute_url) {
    get_absolute_url = get_absolute_url.toString().replace(/[ /\ ]/gi, '');
    $.ajax({
        type: "GET",
        url: get_absolute_url,
        success: function(data) {
            $("#messages-table").empty();
            $(".table-responsive").prepend('<div class="message_detail_all">' +
                '<h2 class="message_title">' + data.message.title + '</h2>' +
                '<div class="sender_and_time">' +
                '<h4 class="message_sender"> TO : ' + data.message.reciver + '</h4>' +
                '<h4 class="message_time">' + data.message.date_message + '</h4>' +
                '</div>' +
                '<div class="message_content">' +
                '<p>' + data.message.content_message + '</p>' +
                '</div>' +
                '</div>'
            )
        }
    });
};






