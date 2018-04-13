<!--
function isMobile(){
    os = navigator.appVersion;
    if ((os.indexOf("Mac")!=-1)||(os.indexOf("OS X")!=-1)||(os.indexOf("Android")!=-1)){
	return true;
    }
    else{return false}
}
function changeStyle(){
    if(!isMobile()){
	var Style = document.getElementById("style");
	Style.href="style/style_pc.css"
    }
}
window.onload = changeStyle;
//--> 
