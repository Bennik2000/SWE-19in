var text = '{"email": "jonas1.hille@email.com", "name": "Jonas1 Hille 2","password": "123456"}';
function createAccount() {
    var newEmail = document.getElementById("email");
    var firstName = document.getElementById("firstname");
    var secondName = document.getElementById("secondname");
    var newPassword = document.getElementById("password");
    var newPassword2 = document.getElementById("password2");
    var newToken = document.getElementById("token");
    if (newPassword.value != newPassword2.value) {
        alert("Passwörter stimmen nicht überein. \n Bitte überprüfen!");
        newEmail.value = newEmail.value;
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
        var xhttp = new XMLHttpRequest();
        var url = "/user";
        xhttp.open("POST", url, true);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(myJSON);
        if (true) {
            alert("Account erfolgreich angelegt!");
            window.location.href = "/#";
        }
        else {
            alert("Account anlegen fehlgeschlagen!");
        }
    }
}
