let frontendHelper = new FrontendHelper()

function setNewPassword() {
    var newPassword1 = document.getElementById("newPassword1") as HTMLInputElement;
    var newPassword2 = document.getElementById("newPassword2") as HTMLInputElement;
    var token = document.getElementById("token") as HTMLElement;

    if((newPassword1.value != newPassword2.value) && newPassword1.value != "") {
        alert("Passwörter stimmen nicht überein. \n Bitte überprüfen!"); 
        return;  
    }
    
    var obj = {};
        obj["password"] = newPassword1.value;
        obj["token"] = token.innerHTML;

        function myOnLoadFunction(response) {
            if (response == null) {
                alert("Kommunikation mit Server fehlgeschlagen!");
                return;
            }
            else if(response.success) { // The response accesses "success:" of the responded JSON Object
                alert("Passwort erfolgreich geändert!"); 
                window.location.href = "/#";
            }
            else
            {
                alert("Passwort ändern fehlgeschlagen!" + "\n➔ " + response.errors[0].title + ".");
            }
        }

        frontendHelper.makeHttpRequest("POST", "/users/reset_password", obj, myOnLoadFunction);
}

function showPassword() {
    var x = document.getElementById("newPassword1") as HTMLInputElement;
    var x2 = document.getElementById("newPassword2") as HTMLInputElement;
    if (x.type === "password") {
      x.type = "text";
      x2.type = "text";
    } else {
      x.type = "password";
      x2.type = "password";
    }
  }