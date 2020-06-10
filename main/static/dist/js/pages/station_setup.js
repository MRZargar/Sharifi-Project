document.getElementById('id_description').addEventListener('keypress',function(e){
     if (isEnglish(e.charCode))
       $("#id_description").css("direction", 'ltr');
     else if(isPersian(e.key))
       $("#id_description").css("direction", 'rtl');
});
$("#id_description").bind("paste", function(e){
    var pastedData = e.originalEvent.clipboardData.getData('text');
    	isStringPersian1(pastedData);
} );id_description

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
			$("#id_description").css("direction", 'rtl');
			break;
		}
	}
}

document.getElementById('id_station_name').addEventListener('keypress',function(e){
     if (isEnglish(e.charCode))
       $("#id_station_name").css("direction", 'ltr');
     else if(isPersian(e.key))
       $("#id_station_name").css("direction", 'rtl');
});
$("#id_station_name").bind("paste", function(e){
    var pastedData = e.originalEvent.clipboardData.getData('text');
    	isStringPersian2(pastedData);
} );id_description

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
			$("#id_station_name").css("direction", 'rtl');
			break;
		}
	}
}


document.getElementById('id_address').addEventListener('keypress',function(e){
     if (isEnglish(e.charCode))
       $("#id_address").css("direction", 'ltr');
     else if(isPersian(e.key))
       $("#id_address").css("direction", 'rtl');
});
$("#id_address").bind("paste", function(e){
    var pastedData = e.originalEvent.clipboardData.getData('text');
    	isStringPersian3(pastedData);
} );id_description

function isEnglish(charCode){
		return (charCode >= 97 && charCode <= 122) || (charCode>=65 && charCode<=90);
}	

function isPersian(key){
	var p = /^[\u0600-\u06FF\s]+$/;    
	return p.test(key) && key!=' ';
}

function isStringPersian3(strings){
	for (i in strings){
		if (isPersian(strings[i])){
			$("#id_address").css("direction", 'rtl');
			break;
		}
	}
}

