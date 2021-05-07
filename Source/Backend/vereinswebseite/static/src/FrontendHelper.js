"use strict";
exports.__esModule = true;
exports.frontendHelper = void 0;
var FrontendHelper = /** @class */ (function () {
    function FrontendHelper() {
        this.isTesting = false;
        this.testRequestCallback = null;
    }
    FrontendHelper.prototype.validateEmail = function (email) {
        var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    };
    FrontendHelper.prototype.makeHttpRequest = function (request, route, data, onloadFunction, isSendingJSON) {
        if (isSendingJSON === void 0) { isSendingJSON = true; }
        if (!this.isTesting) {
            var xhttp = new XMLHttpRequest();
            xhttp.open(request, route, true);
            if (isSendingJSON) {
                xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                data = JSON.stringify(data);
            }
            xhttp.responseType = "json";
            xhttp.send(data);
            xhttp.onload = function () {
                onloadFunction(xhttp.response);
            };
        }
        else {
            if (this.testRequestCallback != null) {
                var response = this.testRequestCallback(request, route, data);
                onloadFunction(response);
            }
        }
    };
    return FrontendHelper;
}());
exports.frontendHelper = new FrontendHelper();
