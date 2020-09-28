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


document.getElementById('id_title').addEventListener('keypress',function(e){
     if (isEnglish(e.charCode))
       $("#id_title").css("direction", 'ltr');
     else if(isPersian(e.key))
       $("#id_title").css("direction", 'rtl');
});
$("#id_title").bind("paste", function(e){
    var pastedData = e.originalEvent.clipboardData.getData('text');
        isStringPersian2(pastedData);
} );

function isEnglish(charCode){
        return (charCode >= 97 && charCode <= 122) || (charCode>=65 && charCode<=90);
}   

function isPersian(key){
    var p = /^[\u0600-\u06FF\s]+$/;    
    return p.test(key) && key!=' ';
}

function isStringPersian2(strings){
    for (i in strings){
        if (isPersian(strings[i])){
            $("#id_title").css("direction", 'rtl');
            break;
        }
    }
}


document.getElementById('id_send_content').addEventListener('keypress',function(e){
     if (isEnglish(e.charCode))
       $("#id_send_content").css("direction", 'ltr');
     else if(isPersian(e.key))
       $("#id_send_content").css("direction", 'rtl');
});
$("#id_send_content").bind("paste", function(e){
    var pastedData = e.originalEvent.clipboardData.getData('text');
        isStringPersian1(pastedData);
} );

function isEnglish(charCode){
        return (charCode >= 97 && charCode <= 122) || (charCode>=65 && charCode<=90);
}   

function isPersian(key){
    var p = /^[\u0600-\u06FF\s]+$/;    
    return p.test(key) && key!=' ';
}

function isStringPersian1(strings){
    for (i in strings){
        if (isPersian(strings[i])){
            $("#id_send_content").css("direction", 'rtl');
            break;
        }
    }
}










