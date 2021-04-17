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
function email_save() {
}
function password_save() {
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
        response.forEach(function (element) {
            var token = document.createElement("a");
            token.innerHTML = element;
            var button = document.createElement("button");
            button.type = "button";
            button.classList.add("btn");
            button.classList.add("btn-secondary");
            button.classList.add("ml-2");
            button.innerHTML = "Löschen";
            var listItem = document.createElement("li");
            listItem.classList.add("list-group-item");
            listItem.appendChild(button);
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
function delete_access_token() {
    function reqListener() {
        var response = this.response;
    }
    //let xhttp = new XMLHttpRequest();
    //xhttp.addEventListener("load",reqListener)
    //xhttp.open("GET","/users/personal_info",true);
    //xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    //xhttp.responseType="json";
    //xhttp.send();
}
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
