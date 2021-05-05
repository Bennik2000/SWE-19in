
let frontendHelper = new FrontendHelper()


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
function delete_account(){
    function myOnloadFunction(response){
        if (response.success!=true){
            window.location.href="/login"
        }
        else{
        alert("Account löschen fehlgeschlagen! Bitte versuchen Sie es erneut!"); 
        }
        
    }
    let jsonObj={};
    frontendHelper.makeHttpRequest("DELETE", "/api/users/delete", jsonObj, myOnloadFunction);
}
function logout(){
    function myOnloadFunction(response){
        if(response){
            if (response.success==true){
                window.location.href="/login"
            
            }else{
            alert("Logout fehlgeschlagen! Bitte versuchen Sie es erneut!")
            }  
        }else{
            alert("Kommunikation mit Server fehlgeschlagen!")
        }      
    }
    let jsonObj={};
    frontendHelper.makeHttpRequest("POST", "/api/users/logout", jsonObj, myOnloadFunction);
}

function email_save() {
    let newEmail=document.getElementById("current_email_new") as HTMLInputElement;
    let currentEmail=document.getElementById("current_email");
    let oldEmail=document.getElementById("old_email");   

    if (!frontendHelper.validateEmail(newEmail.value)) {
        alert("E-Mail nicht valide! Bitte überprüfen");
        return;
    }else if(newEmail.value == currentEmail.innerHTML){
        alert("Fehler! Die E-Mail Adresse ist identisch mit der aktuell Verwendeten");
        return;
    }
    function myOnloadFunction(response){
        if(response){
            if (response.success==true){
            alert("E-Mail wurde erfolgreich geändert!")
            oldEmail.innerHTML=newEmail.value
            currentEmail.innerHTML=newEmail.value
            newEmail.value="";
            }else{
            alert("Fehlgeschlagen! Bitte versuchen Sie es erneut!")
            }  
        }else{
            alert("Kommunikation mit Server fehlgeschlagen!");
        }     
         
        
    }
    let jsonObj={};
    jsonObj["email"]= newEmail.value;

    frontendHelper.makeHttpRequest("POST", "/api/users/change_email", jsonObj, myOnloadFunction);
}

function password_save() {
    
    var renamenewPassword = document.getElementById("rename_new_password") as HTMLInputElement;
    var renamenewPassword2 = document.getElementById("rename_new_password2") as HTMLInputElement;

    if(renamenewPassword.value != renamenewPassword2.value) {
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
        else if(response.success) { // The response accesses "success:" of the responded JSON Object
            alert("Passwort erfolgreich geändert"); 
        }
        else
        {
            alert("Passwort ändern fehlgeschlagen!" + "\n➔ " + response.errors[0].title + ".");
        }
    }
    frontendHelper.makeHttpRequest("POST", "/api/users/change_password", jsonObj, myOnloadFunction);
    }
}



function reload(x:number){
    let templates=[document.getElementById("base_template"),document.getElementById("password_template"),
                document.getElementById("email_template"),document.getElementById("passcode_template"),
                document.getElementById("berechtigung_template")];
    
    
    templates.forEach(element => {
        element.classList.add('d-none');
    });
    templates[x].classList.remove('d-none');
    
    switch(x){
        case 0:
            if(window.history.state!=x){
                history.pushState('0', 'Base');
            }
            break;
        case 1:
            if(window.history.state!=x){
                history.pushState('1', 'Email');
            }
            break;
        case 2:
            if(window.history.state!=x){
                history.pushState('2', 'Password');
            }
            break;
        case 3:
            if(window.history.state!=x){
                history.pushState('3', 'Passcode');   
            }
            get_access_token();
            break;
        case 4:
            if(window.history.state!=x){
                history.pushState('4', 'Berechtigung');
            }
            get_users();
            break;
    }

}
function get_access_token(){

    let tokenlist=document.getElementById("acces_tokens_list");

    function myOnloadFunction(response){

        while(tokenlist.lastChild){
            tokenlist.removeChild(tokenlist.lastChild);
        }

        response.tokens.forEach(element => {
            let token=document.createElement("a");
            token.innerHTML=element;
    
            /*let button=document.createElement("button");
            button.type="button";
            button.classList.add("btn");
            button.classList.add("btn-secondary");
            button.classList.add("ml-2");
            button.setAttribute("onclick","delete_access_token(this);");
            button.innerHTML="Löschen";*/
    
            let listItem=document.createElement("li");
            listItem.classList.add("list-group-item");
            //listItem.appendChild(button);
            listItem.appendChild(token);
    
            tokenlist.appendChild(listItem);
        });
        
    }
    let jsonObj={};
    frontendHelper.makeHttpRequest("GET", "/api/accessToken", jsonObj, myOnloadFunction);

}
function get_users(){

    let userList=document.getElementById("user_list");

    function myOnloadFunction(response){

        while(userList.lastChild){
            userList.removeChild(userList.lastChild);
        }

        response.forEach(element => {
            let username=document.createElement("p");
            let nh5=document.createElement("h6");
            let na=document.createElement("a");
            nh5.innerHTML="Name: ";
            nh5.style.display="inline";
            username.appendChild(nh5);
            na.innerHTML=element.name;
            username.appendChild(na);

            let usermail=document.createElement("p");
            let eh5=document.createElement("h6");
            let ea=document.createElement("a");
            eh5.innerHTML="Email: ";
            eh5.style.display="inline";
            usermail.appendChild(eh5);
            ea.innerHTML=element.email;
            usermail.appendChild(ea);

            let userid=document.createElement("p");
            let ih5=document.createElement("h6");
            let ia=document.createElement("a");
            ih5.innerHTML="ID: ";
            ih5.style.display="inline";
            userid.appendChild(ih5);
            ia.innerHTML=element.id;
            userid.appendChild(ia);

    
            let listItem=document.createElement("li");
            listItem.classList.add("list-group-item");
            listItem.appendChild(username);
            listItem.appendChild(usermail);
            listItem.appendChild(userid);

            userList.appendChild(listItem);
        });
        
    }
    let jsonObj={};
    frontendHelper.makeHttpRequest("GET", "/api/users", jsonObj, myOnloadFunction);
}
function delete_access_token(elem: Element ){
  /*  function myOnloadFunction(response){
        if (response.success=true){
            get_access_token();
        }
    }

    let jsonObj={};
    jsonObj["token"]=elem.parentElement.getElementsByTagName("a")[0].innerHTML
    frontendHelper.makeHttpRequest("DELETE", "/api/accessToken/delete", jsonObj, myOnloadFunction);
*/}
function get_user_info(){
    function myOnloadFunction(response){
        document.getElementById("Username").innerHTML=response.name;
        document.getElementById("current_email").innerHTML=response.email;
        document.getElementById("old_email").innerHTML=response.email;
        
    }
    let jsonObj ={};
    frontendHelper.makeHttpRequest("GET", "/api/users/personal_info", jsonObj, myOnloadFunction);
}
window.addEventListener('popstate', function (popstateEvent) {
    reload(Number(window.history.state));

});

window.onload=function(){
    get_user_info();
}
