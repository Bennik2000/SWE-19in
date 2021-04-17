var frontendHelper = new FrontendHelper();
function createAccount() {
    var newEmail = document.getElementById("email");
    var firstName = document.getElementById("firstname");
    var secondName = document.getElementById("secondname");
    var newPassword = document.getElementById("password");
    var newPassword2 = document.getElementById("password2");
    var newToken = document.getElementById("token");
    if (newPassword.value != newPassword2.value) {
        alert("Passwörter stimmen nicht überein. \n Bitte überprüfen!");
        return;
    }
    if (!frontendHelper.validateEmail(newEmail.value)) {
        alert("Email nicht valide! Bitte überprüfen");
        return;
    }
    if (newEmail.value != "" && firstName.value != "" && secondName.value != "" &&
        newPassword.value != "" && newPassword2.value != "" && newToken.value != "") {
        var obj = {};
        obj["email"] = newEmail.value;
        obj["name"] = firstName.value + " " + secondName.value;
        obj["password"] = newPassword.value;
        obj["token"] = newToken.value;
        var myJSON = JSON.stringify(obj);
        function myOnloadFunction() {
            if (this.response == null) {
                alert("Kommunikation mit Server fehlgeschlagen!");
                return;
            }
            else if (this.response.success) { // The response accesses "success:" of the responded JSON Object
                alert("Account erfolgreich angelegt!");
                window.location.href = "/#";
            }
            else {
                alert("Account anlegen fehlgeschlagen!" + "\n➔ " + this.response.errors[0].title + ".");
            }
        }
        frontendHelper.manageXMLHttpRequest("POST", "/users", myJSON, myOnloadFunction);
    }
}
function cancelCreateAccount() {
    window.location.href = "/#";
}
