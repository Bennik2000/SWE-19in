var frontendHelper = new FrontendHelper();
function bio_edit() {
    if (document.getElementById("head_description").hasAttribute('readonly')) {
        document.getElementById("head_description").removeAttribute('readonly');
        document.getElementById("head_description_save").removeAttribute('disabled');
        document.getElementById("head_description_edit").setAttribute('disabled', '');
    }
}
function bio_save() {
    if (!document.getElementById("head_description").hasAttribute('readonly')) {
        document.getElementById("head_description").setAttribute('readonly', '');
        document.getElementById("head_description_edit").removeAttribute('disabled');
        document.getElementById("head_description_save").setAttribute('disabled', '');
    }
}
function delete_account() {
    function reqListener() {
        var response = this.response;
        if (response.success != true) {
        }
        window.location.href = "/";
    }
    var xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", reqListener);
    xhttp.open("DELETE", "/users/delete", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send();
}
function logout() {
    function reqListener() {
        var response = this.response;
        if (response.success = true) {
            //window.location.href="/login"
        }
    }
    var xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", reqListener);
    xhttp.open("POST", "/users/logout", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send();
}
function email_save() {
    /*let newEmail=document.getElementById("current_email_new");
    function reqListener(){
        let response = this.response
        document.getElementById("Username").innerHTML=response.name;
        document.getElementById("current_email").innerHTML=response.email;
        
    }
    let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load",reqListener)
    xhttp.open("GET","/users/personal_info",true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    let request={};
    request["email"]=
    xhttp.responseType="json";
    xhttp.send();*/
}
function password_save() {
    var renamenewPassword = document.getElementById("rename_new_password");
    var renamenewPassword2 = document.getElementById("rename_new_password2");
    if (renamenewPassword.value != renamenewPassword2.value) {
        alert("Passwörter stimmen nicht überein. \n Bitte überprüfen!");
        return;
    }
    if (renamenewPassword.value != "" && renamenewPassword2.value != "" && renamenewPassword.value == renamenewPassword2.value) {
        var jsonObj = {};
        jsonObj["password"] = renamenewPassword.value;
        function myOnloadFunction(response) {
            if (response == null) {
                alert("Kommunikation mit Server fehlgeschlagen!");
                return;
            }
            else if (response.success) { // The response accesses "success:" of the responded JSON Object
                alert("Passwort erfolgreich geändert");
                window.location.href = "/#";
            }
            else {
                alert("Passwort ändern fehlgeschlagen!" + "\n➔ " + response.errors[0].title + ".");
            }
        }
        frontendHelper.makeHttpRequest("POST", "/users/change_password", jsonObj, myOnloadFunction);
    }
}
function reload(x) {
    var templates = [document.getElementById("base_template"), document.getElementById("password_template"),
        document.getElementById("email_template"), document.getElementById("passcode_template"),
        document.getElementById("berechtigung_template")];
    templates.forEach(function (element) {
        element.classList.add('d-none');
    });
    templates[x].classList.remove('d-none');
    switch (x) {
        case 0:
            if (window.history.state != x) {
                history.pushState('0', 'Base');
            }
            break;
        case 1:
            if (window.history.state != x) {
                history.pushState('1', 'Email');
            }
            break;
        case 2:
            if (window.history.state != x) {
                history.pushState('2', 'Password');
            }
            break;
        case 3:
            if (window.history.state != x) {
                history.pushState('3', 'Passcode');
            }
            get_access_token();
            break;
        case 4:
            if (window.history.state != x) {
                history.pushState('4', 'Berechtigung');
            }
            get_users();
            break;
    }
}
function get_access_token() {
    var tokenlist = document.getElementById("acces_tokens");
    function reqListener() {
        var response = this.response;
        while (tokenlist.lastChild) {
            tokenlist.removeChild(tokenlist.lastChild);
        }
        response.tokens.forEach(function (element) {
            var token = document.createElement("a");
            token.innerHTML = element;
            /*let button=document.createElement("button");
            button.type="button";
            button.classList.add("btn");
            button.classList.add("btn-secondary");
            button.classList.add("ml-2");
            button.setAttribute("onclick","delete_access_token(this);");
            button.innerHTML="Löschen";*/
            var listItem = document.createElement("li");
            listItem.classList.add("list-group-item");
            //listItem.appendChild(button);
            listItem.appendChild(token);
            tokenlist.appendChild(listItem);
        });
    }
    var xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", reqListener);
    xhttp.open("GET", "/accessToken", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.responseType = "json";
    xhttp.send();
}
function get_users() {
    var userList = document.getElementById("berechtigung_template");
    function reqListener() {
        var response = this.response;
        while (userList.lastChild) {
            userList.removeChild(userList.lastChild);
        }
        response.forEach(function (element) {
            var username = document.createElement("p");
            var nh5 = document.createElement("h6");
            var na = document.createElement("a");
            nh5.innerHTML = "Name: ";
            nh5.style.display = "inline";
            username.appendChild(nh5);
            na.innerHTML = element.name;
            username.appendChild(na);
            var usermail = document.createElement("p");
            var eh5 = document.createElement("h6");
            var ea = document.createElement("a");
            eh5.innerHTML = "Email: ";
            eh5.style.display = "inline";
            usermail.appendChild(eh5);
            ea.innerHTML = element.email;
            usermail.appendChild(ea);
            var userid = document.createElement("p");
            var ih5 = document.createElement("h6");
            var ia = document.createElement("a");
            ih5.innerHTML = "ID: ";
            ih5.style.display = "inline";
            userid.appendChild(ih5);
            ia.innerHTML = element.id;
            userid.appendChild(ia);
            var listItem = document.createElement("li");
            listItem.classList.add("list-group-item");
            listItem.appendChild(username);
            listItem.appendChild(usermail);
            listItem.appendChild(userid);
            userList.appendChild(listItem);
        });
    }
    var xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", reqListener);
    xhttp.open("GET", "/users", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.responseType = "json";
    xhttp.send();
}
/*function delete_access_token(elem: Element ){
    function reqListener(){
        let response = this.response
        if (response.success=true){
            get_access_token();
        }
        
    }
    let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load",reqListener)
    xhttp.open("DELETE","/accessToken/delete",true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    let request={};
    request["token"]=elem.parentElement.getElementsByTagName("a")[0].innerHTML
    xhttp.responseType="json";
    xhttp.send();

}*/
function get_user_info() {
    function reqListener() {
        var response = this.response;
        document.getElementById("Username").innerHTML = response.name;
        document.getElementById("current_email").innerHTML = response.email;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", reqListener);
    xhttp.open("GET", "/users/personal_info", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.responseType = "json";
    xhttp.send();
}
window.addEventListener('popstate', function (popstateEvent) {
    reload(Number(window.history.state));
});
window.onload = function () {
    get_user_info();
};
