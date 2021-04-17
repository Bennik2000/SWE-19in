class FrontendHelper {

    validateEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    manageXMLHttpRequest(request: string, route: string, json: string, onloadFunction){
        var xhttp = new XMLHttpRequest();
        xhttp.open(request, route, true);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.responseType = "json";
        xhttp.send(json);
        xhttp.onload = onloadFunction;
    }

}
