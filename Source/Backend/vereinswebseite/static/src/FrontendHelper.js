var FrontendHelper = /** @class */ (function () {
    function FrontendHelper() {
    }
    FrontendHelper.prototype.validateEmail = function (email) {
        var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    };
    FrontendHelper.prototype.manageXMLHttpRequest = function (request, route, json, onloadFunction) {
        var xhttp = new XMLHttpRequest();
        xhttp.open(request, route, true);
        xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhttp.responseType = "json";
        xhttp.send(json);
        xhttp.onload = onloadFunction;
    };
    return FrontendHelper;
}());
