// $(document).ready(function() {
//     $("#createButton").click(function(e) {
//         e.preventDefault();
//         var serializedData =
//             $("#createUser").serialize();

//         $.ajax({
//             url: $("createUser").data('url'),
//             data: serializedData,
//             type: 'post',
//             success: function(response) {
//                 $(".messagelist").css('display', 'block');
//                 $(".SignUp--user").css('top', '500px');
//             }
//         })
//         $("#createUser")[0].reset();
//     });
// });