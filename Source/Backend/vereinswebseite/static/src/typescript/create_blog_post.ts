let frontendHelper = new FrontendHelper()
var isShowingPreview: Boolean = false;

function swapShowingPreview() {
    var markdown = document.getElementById("markdown") as HTMLInputElement;
    var jsonObj = {};
        jsonObj["content"] = markdown.value;

    if(!isShowingPreview && markdown.value != "") {
        
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

function saveCreatedBlogPost() {
    var title = document.getElementById("title") as HTMLInputElement;
    var markdown = document.getElementById("markdown") as HTMLInputElement;
    var jsonObj = {};
    jsonObj["title"] = title.value;
    jsonObj["content"] = markdown.value;

    function myOnloadFunction(response) {
        if(response == null)
        {
            alert("Kommunikation mit Server fehlgeschlagen!");
            return;
        }
        else if (response.success) {
            window.location.href = "/#"; //TODO: Link to the blog post overview of all post
        }
        else {
            alert("Speichern fehlgeschlagen!");
        }
    }
    frontendHelper.makeHttpRequest("POST", "/blog_posts", jsonObj, myOnloadFunction);
}