var frontendHelper = new FrontendHelper();
function resetPasswordRequest() {
    var email = document.getElementById("email");
    if (!frontendHelper.validateEmail(email.value)) {
        alert("Email nicht valide! Bitte überprüfen");
        return;
    }
    var jsonObj = {};
    jsonObj["email"] = email.value;
    function myOnloadFunction(response) {
        if (response == null) {
            alert("Kommunikation mit Server fehlgeschlagen!");
            return;
        }
        else if (response.success) { // The response accesses "success:" of the responded JSON Object
            alert("Email wurde versendet!");
            window.location.href = "/#";
        }
        else {
            window.location.href = "/#";
        }
    }
    frontendHelper.makeHttpRequest("POST", "/users/request_new_password", jsonObj, myOnloadFunction);
}
