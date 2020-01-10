var subjElem = document.querySelector("#subj_id");
var courseNumElem = document.querySelector("#crse_id");
var subj = findGetParameter("subj");


if( subj != null ) {
	subjElem.value = subj;
	
	var num = findGetParameter("num");
	if( num != null )
		courseNumElem.value = num;
		
	document.querySelector("form").submit();
}



function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    var items = location.search.substr(1).split("&");
    for (var index = 0; index < items.length; index++) {
        tmp = items[index].split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    }
    return result;
}