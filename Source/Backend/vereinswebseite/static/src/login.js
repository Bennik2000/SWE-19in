function login() {
    var email = document.getElementById("email");
    var password = document.getElementById("password");
    if (!validateEmail(email.value)) {
        alert("Email nicht valide! Bitte überprüfen");
        return;
    }
    if (email.value != "" && password.value != "") {
        var obj = {};
        obj["email"] = email.value;
        obj["password"] = password.value;
        var myJSON = JSON.stringify(obj);
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/users/login", true);
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
                window.location.href = "/#";
            }
            else {
                alert("Login fehlgeschlagen!" + "\n➔ " + this.response.errors[0].title + ".");
            }
        };
    }
}
function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
