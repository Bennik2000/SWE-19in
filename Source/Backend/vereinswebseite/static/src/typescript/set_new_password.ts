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
        obj["token"] = token.innerText;
        var myJSON = JSON.stringify(obj);
    
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/users", true);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.responseType = "json";
        xhttp.send(myJSON);
        
        // Read the backend-response
        xhttp.onload = function(e) {
            if (this.response == null) {
                alert("Kommunikation mit Server fehlgeschlagen!");
                return;
            }
            else if(this.response.success) { // The response accesses "success:" of the responded JSON Object
                alert("Passwort erfolgreich geändert!"); 
                window.location.href = "/#";
            }
            else
            {
                alert("Passwort ändern fehlgeschlagen!" + "\n➔ " + this.response.errors[0].title + ".");
            }
        } 
        

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