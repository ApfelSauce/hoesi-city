<!--
function key(st){
    var check=document.getElementById("keybC");
    var box = document.getElementById("logB");
    if (st == 0){
	//create a keyboard
	var keyboard = '<table>'+
	    '<tr><td><input type="button" onclick="keyHit(1)" value="1" class="key"></input></td>'+
	    '<td><input type="button" onclick="keyHit(2)" value="2" class="key"></input></td>'+
	    '<td><input type="button" onclick="keyHit(3)" value="3" class="key"></input></td></tr>'+
	    '<tr><td><input type="button" onclick="keyHit(4)" value="4" class="key"></input></td>'+
	    '<td><input type="button" onclick="keyHit(5)" value="5" class="key"></input></td>'+
	    '<td><input type="button" onclick="keyHit(6)" value="6" class="key"></input></td></tr>'+
	    '<tr><td><input type="button" onclick="keyHit(7)" value="7" class="key"></input></td>'+
	    '<td><input type="button" onclick="keyHit(8)" value="8" class="key"></input></td>'+
	    '<td><input type="button" onclick="keyHit(9)" value="9" class="key"></input></td></tr>'+
	    '<tr><td></td><td><input type="button" onclick="keyHit(0)" value="0" class="key"></input></td><td></td></tr>'
	'</table>';
	box.innerHTML = keyboard;
	check.setAttribute("onchange","key(1)");
    }else{
	box.innerHTML = "";
	check.setAttribute("onchange","key(0)");
    }
}
function keyHit(Key){
    var ret = document.getElementById("pas");
    pas.value+=Key;
}
//--> 
