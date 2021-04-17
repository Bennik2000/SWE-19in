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
    function reqListener(){
        let response = this.response
        if (response.success!=true){
            
        }
        window.location.href="/"
    }
    let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load",reqListener)
    xhttp.open("DELETE", "/users/delete",true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send();
}

function email_save() {
}

function password_save() {
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
            break;
        case 4:
            if(window.history.state!=x){
                history.pushState('4', 'Berechtigung');
            }
            break;
    }

}

function get_user_info(){
    function reqListener(){
        let response = this.response
        document.getElementById("Username").innerHTML=response.name;
        document.getElementById("current_email").innerHTML=response.email;
        
    }
    let xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load",reqListener)
    xhttp.open("GET","/users/personal_info",true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.responseType="json";
    xhttp.send();
}
window.addEventListener('popstate', function (popstateEvent) {
    reload(Number(window.history.state));

});

window.onload=function(){
    get_user_info();
}
