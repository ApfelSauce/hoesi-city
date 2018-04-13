<!--
function snap(){
    var a = getXfromSearch("id");
    var hidd = document.getElementById("ID");
    hidd.value=a;
}
function getXfromSearch(X){
    var z = location.search;
    z = z.substring(1)
    var x = z.split("&");
    var t = false;
    var y = "tree";
    for(var i = 0; i < x.length; i++){
	if(x[i].split("=")[0] == X){
	    y = x[i];
	    t = true;
	}
    }
    if(t!=true){return false};
    x = y.split("=");
    z = x[1];
    return z;    
}
window.addEventListener('load', snap);
//--> 
