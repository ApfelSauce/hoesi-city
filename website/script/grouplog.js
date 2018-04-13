<!--
function logG(){
    It = getXfromSearch("id");
    document.cookie = "id="+ It;
    document.cookie = "pw="+ document.getElementById("pw").value;
    location.reload();
}
function logOut(){
    deleteCokieName("id");
    deleteCokieName("pw");
    location.reload();
}
function deleteCokieName(name) {
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};
//--> 
