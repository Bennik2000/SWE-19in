class FrontendHelper {

    isTesting: Boolean = false;
    testRequestCallback = null;

    validateEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    makeHttpRequest(request: string, route: string, data , onloadFunction, isSendingJSON = true){
        if (!this.isTesting) {
            var xhttp = new XMLHttpRequest();
            xhttp.open(request, route, true);

            if(isSendingJSON){
                xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                data = JSON.stringify(data);
            }

            xhttp.responseType = "json";
            xhttp.send(data);
            xhttp.onload = () => {
                onloadFunction(xhttp.response)
            };
        }
        else {
            if (this.testRequestCallback != null)
            {
                var response = this.testRequestCallback(request, route, data);
                onloadFunction(response);
            }
        }
    }

}
export const frontendHelper = new FrontendHelper();
