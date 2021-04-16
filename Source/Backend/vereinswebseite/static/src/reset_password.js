"use strict";
exports.__esModule = true;
exports.validateEmail = void 0;
function resetPasswordRequest() {
    var email = document.getElementById("email");
    if (!validateEmail(email.value)) {
        alert("Email nicht valide! Bitte überprüfen");
        return;
    }
    var obj = {};
    obj["email"] = email.value;
    var myJSON = JSON.stringify(obj);
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/users/request_new_password", true);
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
            alert("Email wurde versendet!");
            window.location.href = "/#";
        }
        else {
            window.location.href = "/#";
        }
    };
}
function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
exports.validateEmail = validateEmail;
