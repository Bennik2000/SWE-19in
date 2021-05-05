let frontendHelper = new FrontendHelper()


function login() {
    var email = document.getElementById("email") as HTMLInputElement;
    var password = document.getElementById("password") as HTMLInputElement;

    if (!frontendHelper.validateEmail(email.value)) {
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
                window.location.href = "/account";
            }
            else 
            {
                alert("Login fehlgeschlagen!" + "\n➔ " + response.errors[0].title + ".");
            }
        }
        frontendHelper.makeHttpRequest("POST", "/api/users/login", jsonObj, myOnloadFunction); 
    }
}