$(document).ready(function() {
    $("#createButton").click(function() {
        var serializedData =
            $("#createUser").serialize();

        $.ajax({
            url: $("createUser").data('url'),
            data: serializedData,
            type: 'post',
            success: function(response) {
                $(".messagelist").css('display', 'block');
                $(".SignUp--user").css('top', '50px');
            }
        })
        $("#createUser")[0].reset();
    });
});