var frontendHelper = new FrontendHelper();
function setNewPassword() {
    var newPassword1 = document.getElementById("newPassword1");
    var newPassword2 = document.getElementById("newPassword2");
    var token = document.getElementById("token");
    if ((newPassword1.value != newPassword2.value) && newPassword1.value != "") {
        alert("Passwörter stimmen nicht überein. \n Bitte überprüfen!");
        return;
    }
    var obj = {};
    obj["password"] = newPassword1.value;
    obj["token"] = token.innerText;
    function myOnLoadFunction(response) {
        if (this.response == null) {
            alert("Kommunikation mit Server fehlgeschlagen!");
            return;
        }
        else if (this.response.success) { // The response accesses "success:" of the responded JSON Object
            alert("Passwort erfolgreich geändert!");
            window.location.href = "/#";
        }
        else {
            alert("Passwort ändern fehlgeschlagen!" + "\n➔ " + this.response.errors[0].title + ".");
        }
    }
    frontendHelper.makeHttpRequest("POST", "/users", obj, myOnLoadFunction);
}
function showPassword() {
    var x = document.getElementById("newPassword1");
    var x2 = document.getElementById("newPassword2");
    if (x.type === "password") {
        x.type = "text";
        x2.type = "text";
    }
    else {
        x.type = "password";
        x2.type = "password";
    }
}
