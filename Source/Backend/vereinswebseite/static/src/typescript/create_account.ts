var text = '{"email": "jonas1.hille@email.com", "name": "Jonas1 Hille 2","password": "123456"}';
function createAccount() {

    var newEmail = document.getElementById("email") as HTMLInputElement;
    var firstName = document.getElementById("firstname") as HTMLInputElement;
    var secondName = document.getElementById("secondname") as HTMLInputElement;
    var newPassword = document.getElementById("password")as HTMLInputElement;
    var newPassword2 = document.getElementById("password2")as HTMLInputElement;
    var newToken = document.getElementById("token")as HTMLInputElement;

    if(newPassword.value != newPassword2.value) {
        alert("Passwörter stimmen nicht überein. \n Bitte überprüfen!"); 
        return;  
    }

    if (!validateEmail(newEmail.value)) {
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
    
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/user", true);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.send(myJSON);

        if(true) {
            alert("Account erfolgreich angelegt!");
            window.location.href = "/#";
        }
        else
        {
            alert("Account anlegen fehlgeschlagen!");
        }
    }

}

function cancelCreateAccount(){
    window.location.href = "/#";
}

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}