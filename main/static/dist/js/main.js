// $('form').on('submit', function(e) {
//     e.preventDefault()
//     $.ajax({
//         type: "POST",
//         url: $(this).attr('action'),
//         data: $('#login_form').serialize(),
//         beforeSend: function(xhr, settings) {
//             var csrftoken = Cookies.get('csrf_token');

//             function csrfSafeMethod(method) {
//                 // these HTTP methods do not require CSRF protection
//                 return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//             }
//             if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//                 xhr.setRequestHeader("X-CSRFToken", csrftoken);
//             }
//         },
//         success: function(response) {
//             if (response['result'] == 'Success!')
//                 window.location = '/';
//             else
//                 alert(response['message']);
//         }
//     });
// });