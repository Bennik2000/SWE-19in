let frontendHelper = new FrontendHelper()
var isShowingPreview: Boolean = false;

function swapShowingPreview() {
    var markdown = document.getElementById("markdown") as HTMLInputElement;
    var jsonObj = {};
        jsonObj["content"] = markdown.value;



    if(!isShowingPreview && markdown.value != "") {
        /*document.getElementById("markdown_preview").innerHTML =
        marked(markdown.value);        
        document.getElementById("swapShowingPreview_button").innerHTML = "Vorschau ausblenden";
        document.getElementById("preview_div").style.display = "block";
        isShowingPreview = true;*/
        
        function myOnloadFunction(response) {
            if(response == null) {
                alert("Kommunikation mit Server fehlgeschlagen!");
                return
            }
            else if (response.success)
            {
                document.getElementById("markdown_preview").innerHTML = response.html;
                document.getElementById("swapShowingPreview_button").innerHTML = "Vorschau ausblenden";
                document.getElementById("preview_div").style.display = "block";
                isShowingPreview = true;
            }
            else {
                alert("Anzeigen der Vorschau fehlgeschlagen!" + "\n➔ " + response.errors[0].title + ".");
            }
    }
    frontendHelper.makeHttpRequest("POST", "/blog_posts/render_preview", jsonObj, myOnloadFunction);

    }
    else{
        document.getElementById("markdown_preview").innerHTML = "";
        document.getElementById("swapShowingPreview_button").innerHTML = "Vorschau anzeigen";        
        document.getElementById("preview_div").style.display = "none";
        isShowingPreview = false;
    }
}