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
function base() {
    document.getElementById("base_template").classList.remove('d-none');
    document.getElementById("email_template").classList.add('d-none');
    document.getElementById("password_template").classList.add('d-none');
    document.getElementById("passcode_template").classList.add('d-none');
    document.getElementById("berechtigung_template").classList.add('d-none');
    if (!(window.history.state == 1)) {
        history.pushState('1', '1');
    }
}
function password() {
    document.getElementById("base_template").classList.add('d-none');
    document.getElementById("email_template").classList.add('d-none');
    document.getElementById("password_template").classList.remove('d-none');
    document.getElementById("passcode_template").classList.add('d-none');
    document.getElementById("berechtigung_template").classList.add('d-none');
    if (!(window.history.state == 2)) {
        history.pushState('2', '2');
    }
}
function email() {
    document.getElementById("base_template").classList.add('d-none');
    document.getElementById("email_template").classList.remove('d-none');
    document.getElementById("password_template").classList.add('d-none');
    document.getElementById("passcode_template").classList.add('d-none');
    document.getElementById("berechtigung_template").classList.add('d-none');
    if (!(window.history.state == 3)) {
        history.pushState('3', '3');
    }
}
function passcode() {
    document.getElementById("base_template").classList.add('d-none');
    document.getElementById("email_template").classList.add('d-none');
    document.getElementById("password_template").classList.add('d-none');
    document.getElementById("passcode_template").classList.remove('d-none');
    document.getElementById("berechtigung_template").classList.add('d-none');
    if (!(window.history.state == 4)) {
        history.pushState('4', '4');
    }
}
function berechtigung() {
    document.getElementById("base_template").classList.add('d-none');
    document.getElementById("email_template").classList.add('d-none');
    document.getElementById("password_template").classList.add('d-none');
    document.getElementById("passcode_template").classList.add('d-none');
    document.getElementById("berechtigung_template").classList.remove('d-none');
    if (!(window.history.state == 5)) {
        history.pushState('5', '5');
    }
}
function email_save() {
}

function password_save() {
}
window.addEventListener('popstate', function (popstateEvent) {
    switch (Number(window.history.state)) {
        case 1:
            base();
            break;
        case 2:
            password();
            break;
        case 3:
            email();
            break;
    }
});
