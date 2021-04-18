"use strict";
exports.__esModule = true;
exports.frontendHelper = void 0;
var FrontendHelper = /** @class */ (function () {
    function FrontendHelper() {
        this.isTesting = false;
        this.testXHRequestCallback = null;
    }
    FrontendHelper.prototype.validateEmail = function (email) {
        var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    };
    FrontendHelper.prototype.manageXMLHttpRequest = function (request, route, json, onloadFunction) {
        if (!this.isTesting) {
            var xhttp = new XMLHttpRequest();
            xhttp.open(request, route, true);
            xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhttp.responseType = "json";
            xhttp.send(JSON.stringify(json));
            xhttp.onload = function () {
                onloadFunction(xhttp.response);
            };
        }
        else {
            if (this.testXHRequestCallback != null) {
                var response = this.testXHRequestCallback(request, route, json);
                onloadFunction(response);
            }
        }
    };
    return FrontendHelper;
}());
exports.frontendHelper = new FrontendHelper();