let frontendHelper = new FrontendHelper()


function login() {
    var email = document.getElementById("email") as HTMLInputElement;
    var password = document.getElementById("password") as HTMLInputElement;

    if (!validateEmail(email.value)) {
        alert("Email nicht valide! Bitte überprüfen");
        return;
    }

    if (email.value != "" && password.value != "") {
        var jsonObj = {};
        jsonObj["email"] = email.value;
        jsonObj["password"] = password.value;
        
        // Read the backend-response
        function myOnloadFunction(response) {
            if (response == null) {
                alert("Kommunikation mit Server fehlgeschlagen!");
                return;
            }
            else if(response.success) { // The response accesses "success:" of the responded JSON Object
                window.location.href = "/#";
            }
            else 
            {
                alert("Benutzername oder Passwort falsch.");
            }
        }
        frontendHelper.makeHttpRequest("POST", "/users/login", jsonObj, myOnloadFunction); 
    }
}

function validateEmail(email) {  // Replace this function with the same function of the FrontendHelper later on
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}