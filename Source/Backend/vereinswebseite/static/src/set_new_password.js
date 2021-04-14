function setNewPassword() {
    var newPassword1 = document.getElementById("newPassword1");
    var newPassword2 = document.getElementById("newPassword2");
    if ((newPassword1.value != newPassword2.value) && newPassword1.value != "") {
        alert("Passwörter stimmen nicht überein. \n Bitte überprüfen!");
        return;
    }
    var obj = {};
    obj["newPassword"] = newPassword1.value;
    var myJSON = JSON.stringify(obj);
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/users", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.responseType = "json";
    xhttp.send(myJSON);
    // Read the backend-response
    xhttp.onload = function (e) {
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
    };
}
