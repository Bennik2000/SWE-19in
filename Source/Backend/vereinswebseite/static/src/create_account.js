var text = '{"email": "jonas1.hille@email.com", "name": "Jonas1 Hille 2","password": "123456"}';
function createAccount() {
    var newEmail = document.getElementById("email");
    var firstname = document.getElementById("firstname");
    var secondname = document.getElementById("secondname");
    var newPassword = document.getElementById("password");
    var newPassword2 = document.getElementById("password2");
    var newToken = document.getElementById("token");
    var field = "my_field_name";
    var obj = {};
    obj["email"] = newEmail;
    obj["name"] = new String(firstname + " " + secondname);
    obj["password"] = newPassword;
    obj["token"] = newToken;
    var myJSON = JSON.stringify(obj);
    console.log(myJSON);
    /*var xhttp = new XMLHttpRequest();
    var url = "/user";
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(myJSON);*/
}
