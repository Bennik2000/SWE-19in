var frontendHelper = new FrontendHelper();
function makeUserListItem(element) {
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
    eh5.innerHTML = "E-Mail: ";
    eh5.style.display = "inline";
    usermail.appendChild(eh5);
    ea.innerHTML = element.email;
    usermail.appendChild(ea);
    var userid = document.createElement("p");
    var rh5 = document.createElement("h6");
    var ra = document.createElement("a");
    rh5.innerHTML = "Role: ";
    rh5.style.display = "inline";
    userid.appendChild(rh5);
    ra.innerHTML = element.roles;
    userid.appendChild(ra);
    var role = document.createElement("p");
    var ih5 = document.createElement("h6");
    var ia = document.createElement("a");
    ih5.innerHTML = "ID: ";
    ih5.style.display = "inline";
    role.appendChild(ih5);
    ia.innerHTML = element.id;
    role.appendChild(ia);
    var roleInput = document.createElement("input");
    roleInput.id = "roleInput" + element.id;
    roleInput.placeholder = "Rolle,...";
    roleInput.style.width = "30vw";
    roleInput.classList.add("form-control");
    roleInput.classList.add("form-control-md");
    var roleButton = document.createElement("button");
    roleButton.classList.add("btn");
    roleButton.classList.add("btn-secondary");
    roleButton.classList.add("mt-2");
    roleButton.id = "role_save" + element.id;
    roleButton.innerHTML = "Setze Rollen";
    roleButton.type = "submit";
    roleButton.setAttribute("onclick", "saveRoles(" + element.id + ");");
    var listItem = document.createElement("li");
    listItem.classList.add("list-group-item");
    listItem.appendChild(username);
    listItem.appendChild(usermail);
    listItem.appendChild(userid);
    listItem.appendChild(role);
    listItem.appendChild(roleInput);
    listItem.appendChild(roleButton);
    return listItem;
}
function saveRoles(id) {
    function myOnloadFunction(response) {
        if (response) {
            if (response.success == true) {
                alert("Rollen wurde erfolgreich ge??ndert!");
                get_users();
            }
            else {
                alert("??ndern der Rollen fehlgeschlagen! Bitte versuchen Sie es erneut!");
            }
        }
        else {
            alert("Kommunikation mit Server fehlgeschlagen!");
        }
    }
    var rolesDoc = document.getElementById("roleInput" + id);
    var roles = rolesDoc.value;
    var role = roles.split(",");
    console.log(role);
    var jsonObj = {};
    jsonObj["user_id"] = id;
    jsonObj["roles"] = role;
    frontendHelper.makeHttpRequest("PUT", "/api/users/user_roles", jsonObj, myOnloadFunction);
}
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
    if (confirm("Wollen Sie Ihren Account wirklich l??schen? Dann dr??cken sie \"OK\"") == true) {
        function myOnloadFunction(response) {
            if (response.success == true) {
                window.location.href = "/login";
            }
            else {
                alert("Account l??schen fehlgeschlagen! Bitte versuchen Sie es erneut!");
            }
        }
        var jsonObj = {};
        frontendHelper.makeHttpRequest("DELETE", "/api/users/delete", jsonObj, myOnloadFunction);
    }
}
function logout() {
    function myOnloadFunction(response) {
        if (response) {
            if (response.success == true) {
                window.location.href = "/login";
            }
            else {
                alert("Logout fehlgeschlagen! Bitte versuchen Sie es erneut!");
            }
        }
        else {
            alert("Kommunikation mit Server fehlgeschlagen!");
        }
    }
    var jsonObj = {};
    frontendHelper.makeHttpRequest("POST", "/api/users/logout", jsonObj, myOnloadFunction);
}
function email_save() {
    var newEmail = document.getElementById("current_email_new");
    var currentEmail = document.getElementById("current_email");
    var oldEmail = document.getElementById("old_email");
    if (!frontendHelper.validateEmail(newEmail.value)) {
        alert("E-Mail nicht valide! Bitte ??berpr??fen");
        return;
    }
    else if (newEmail.value == currentEmail.innerHTML) {
        alert("Fehler! Die E-Mail Adresse ist identisch mit der aktuell Verwendeten");
        return;
    }
    function myOnloadFunction(response) {
        if (response) {
            if (response.success == true) {
                alert("E-Mail wurde erfolgreich ge??ndert!");
                oldEmail.innerHTML = newEmail.value;
                currentEmail.innerHTML = newEmail.value;
                newEmail.value = "";
            }
            else {
                alert("Fehlgeschlagen! Bitte versuchen Sie es erneut!");
            }
        }
        else {
            alert("Kommunikation mit Server fehlgeschlagen!");
        }
    }
    var jsonObj = {};
    jsonObj["email"] = newEmail.value;
    frontendHelper.makeHttpRequest("POST", "/api/users/change_email", jsonObj, myOnloadFunction);
}
function password_save() {
    var renamenewPassword = document.getElementById("rename_new_password");
    var renamenewPassword2 = document.getElementById("rename_new_password2");
    if (renamenewPassword.value != renamenewPassword2.value) {
        alert("Passw??rter stimmen nicht ??berein. \n Bitte ??berpr??fen!");
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
                alert("Passwort erfolgreich ge??ndert");
            }
            else {
                alert("Passwort ??ndern fehlgeschlagen!" + "\n??? " + response.errors[0].title + ".");
            }
        }
        frontendHelper.makeHttpRequest("POST", "/api/users/change_password", jsonObj, myOnloadFunction);
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
    var tokenlist = document.getElementById("acces_tokens_list");
    function myOnloadFunction(response) {
        while (tokenlist.lastChild) {
            tokenlist.removeChild(tokenlist.lastChild);
        }
        response.tokens.forEach(function (element) {
            var token = document.createElement("a");
            token.innerHTML = element;
            var button = document.createElement("button");
            button.type = "button";
            button.classList.add("btn");
            button.classList.add("btn-secondary");
            button.classList.add("ml-2");
            button.setAttribute("onclick", "delete_access_token(this);");
            button.innerHTML = "L??schen";
            var listItem = document.createElement("li");
            listItem.classList.add("list-group-item");
            listItem.appendChild(token);
            listItem.appendChild(button);
            tokenlist.appendChild(listItem);
        });
    }
    var jsonObj = {};
    frontendHelper.makeHttpRequest("GET", "/api/accessToken", jsonObj, myOnloadFunction);
}
function generate_passcode() {
    function myOnloadFunction(response) {
        get_access_token();
    }
    var jsonObj = {};
    frontendHelper.makeHttpRequest("POST", "/api/accessToken", jsonObj, myOnloadFunction);
}
function get_users() {
    var userList = document.getElementById("user_list");
    function myOnloadFunction(response) {
        while (userList.lastChild) {
            userList.removeChild(userList.lastChild);
        }
        response.forEach(function (element) {
            var listItem = makeUserListItem(element);
            userList.appendChild(listItem);
        });
    }
    var jsonObj = {};
    frontendHelper.makeHttpRequest("GET", "/api/users", jsonObj, myOnloadFunction);
}

function delete_access_token(elem) {
      function myOnloadFunction(response){
          if (response.success==true){
              get_access_token();
          }
      }
  
      let jsonObj={};
      jsonObj["token"]=elem.parentElement.getElementsByTagName("a")[0].innerHTML
      frontendHelper.makeHttpRequest("DELETE", "/api/accessToken", jsonObj, myOnloadFunction);
  
}

function get_user_info() {
    function myOnloadFunction(response) {
        document.getElementById("Username").innerHTML = response.name;
        document.getElementById("current_email").innerHTML = response.email;
        document.getElementById("old_email").innerHTML = response.email;
        var roles = response.roles;
        if (roles.includes("Webmaster")) {
            document.getElementById("webmasterOnly").classList.remove("d-none");
        }
    }
    var jsonObj = {};
    frontendHelper.makeHttpRequest("GET", "/api/users/personal_info", jsonObj, myOnloadFunction);
}
window.addEventListener('popstate', function (popstateEvent) {
    reload(Number(window.history.state));
});
window.onload = function () {
    get_user_info();
};
