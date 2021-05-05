class FrontendHelper {

    isTesting: Boolean = false;
    testRequestCallback = null;

    validateEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    makeHttpRequest(request: string, route: string, json: string, onloadFunction){
        if (!this.isTesting) {
            var xhttp = new XMLHttpRequest();
            xhttp.open(request, route, true);
            xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhttp.responseType = "json";
            xhttp.send(JSON.stringify(json));
            xhttp.onload = () => {
                onloadFunction(xhttp.response)
            };
        }
        else {
            if (this.testRequestCallback != null)
            {
                var response = this.testRequestCallback(request, route, json);
                onloadFunction(response);
            }
        }
    }
    
    sendFile(request: string, route: string, formData: FormData, onloadFunction){
        if (!this.isTesting) {
            var xhttp = new XMLHttpRequest();
            xhttp.open(request, route, true);
            xhttp.setRequestHeader("Content-Type", "multipart/form-data");
            xhttp.responseType = "json";
            xhttp.send(formData);
            xhttp.onload = () => {
                onloadFunction(xhttp.response)
            };
        }
        else {
            if (this.testRequestCallback != null)
            {
                var response = this.testRequestCallback(request, route, formData);
                onloadFunction(response);
            }
        }
    }

}
export const frontendHelper = new FrontendHelper();
