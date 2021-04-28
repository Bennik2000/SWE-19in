var frontendHelper = new FrontendHelper();
var isShowingPreview = false;
function swapShowingPreview() {
    var markdown = document.getElementById("markdown");
    if (isShowingPreview) {
        document.getElementById("markdown_preview").innerHTML = "";
        document.getElementById("updatePreview_button").style.display = "none";
        document.getElementById("preview_div").style.display = "none";
        document.getElementById("hidePreview_button").style.display = "none";
        document.getElementById("swapShowingPreview_button").style.display = "block";
        isShowingPreview = false;
        return;
    }
    if (!markdown.value.trim()) { // Check if the markdown is only containing whitespaces
        alert("Um eine Vorschau anzeigen zu lassen bitte Markdown angeben!");
        return;
    }
    var jsonObj = {};
    jsonObj["content"] = markdown.value;
    function myOnloadFunction(response) {
        if (response == null) {
            alert("Kommunikation mit Server fehlgeschlagen!");
            return;
        }
        else if (response.success) {
            document.getElementById("markdown_preview").innerHTML = response.html;
            document.getElementById("updatePreview_button").style.display = "block";
            document.getElementById("preview_div").style.display = "block";
            document.getElementById("swapShowingPreview_button").style.display = "none";
            document.getElementById("hidePreview_button").style.display = "block";
            isShowingPreview = true;
        }
        else {
            alert("Anzeigen der Vorschau fehlgeschlagen!");
        }
    }
    frontendHelper.makeHttpRequest("POST", "/blog_posts/render_preview", jsonObj, myOnloadFunction);
}
function updatePreview() {
    var markdown = document.getElementById("markdown");
    var jsonObj = {};
    jsonObj["content"] = markdown.value;
    if (!markdown.value.trim() && !isShowingPreview) {
        alert("Um eine Vorschau anzeigen zu lassen bitte Markdown angeben!");
        return;
    }
    function myOnloadFunction(response) {
        if (response == null) {
            alert("Kommunikation mit Server fehlgeschlagen!");
            return;
        }
        else if (response.success) {
            document.getElementById("markdown_preview").innerHTML = response.html;
        }
        else {
            alert("Aktualisieren der Vorschau fehlgeschlagen!");
        }
    }
    frontendHelper.makeHttpRequest("POST", "/blog_posts/render_preview", jsonObj, myOnloadFunction);
}
function saveCreatedBlogPost() {
    var title = document.getElementById("title");
    var markdown = document.getElementById("markdown");
    if (title.value.trim() && markdown.value.trim()) // Checking if the strings are containing only whitespaces
     {
        var jsonObj = {};
        jsonObj["title"] = title.value;
        jsonObj["content"] = markdown.value;
        function myOnloadFunction(response) {
            if (response == null) {
                alert("Kommunikation mit Server fehlgeschlagen!");
                return;
            }
            else if (response.success) {
                window.location.href = "/#"; //TODO: Link to the blog post overview of all post
            }
            else {
                alert("Speichern fehlgeschlagen!" + "\n➔ " + response.errors[0].title + ".");
            }
        }
        frontendHelper.makeHttpRequest("POST", "/blog_posts", jsonObj, myOnloadFunction);
    }
    else {
        title.value = title.value.trim();
        markdown.value = markdown.value.trim();
    }
}
function cancelCreateBlogPost() {
    var wantsToCancel = confirm("Der neue Blog Post wird nicht gespeichert. \nTrotzdem fortfahren?");
    if (wantsToCancel) {
        window.history.back();
    }
}
