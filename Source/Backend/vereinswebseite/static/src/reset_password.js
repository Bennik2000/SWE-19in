var frontendHelper = new FrontendHelper();
function resetPasswordRequest() {
    var email = document.getElementById("email");
    if (!frontendHelper.validateEmail(email.value)) {
        alert("Email nicht valide! Bitte überprüfen");
        return;
    }
    var obj = {};
    obj["email"] = email.value;
    var myJSON = JSON.stringify(obj);
    function myOnloadFunction() {
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
    }
    frontendHelper.manageXMLHttpRequest("POST", "/users/request_new_password", myJSON, myOnloadFunction);
}
