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
    xhttp.open("RESET_PASSWORD", "/users", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.responseType = "json";
    xhttp.send(myJSON);
    // Read the backend-response
    xhttp.onload = function (e) {
        if (this.response.success) { // The response accesses "success:" of the responded JSON Object
            alert("Email wurde versendet!");
            window.location.href = "/#";
        }
        else {
            alert("Email konnte nicht gesendet werden" + "\n➔ " + this.response.errors[0].title + ".");
        }
    };
}
function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
