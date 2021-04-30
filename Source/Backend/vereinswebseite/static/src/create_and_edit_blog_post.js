var frontendHelper = new FrontendHelper();
var isShowingPreview = false;
var timer;
var errorMessageCommunicationWithServer = "Kommunikation mit Server fehlgeschlagen!";
var errorMessageSaving = "Speichern fehlgeschlagen!";
var errorMessageNoMarkdownEntered = "Um eine Vorschau anzeigen zu lassen bitte Markdown angeben!";
var errorMessageShowingPreview = "Anzeigen der Vorschau fehlgeschlagen!";
var errorMessageUpdatingPreview = "Aktualisieren der Vorschau fehlgeschlagen!";
var errorMessageUpdatingOrShowingLivePreview = "Live-Vorschau: Anzeigen/Aktualisieren fehlgeschlagen!";
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
        alert(errorMessageNoMarkdownEntered);
        return;
    }
    var jsonObj = {};
    jsonObj["content"] = markdown.value;
    function myOnloadFunction(response) {
        if (response == null) {
            alert(errorMessageCommunicationWithServer);
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
            alert(errorMessageShowingPreview);
        }
    }
    frontendHelper.makeHttpRequest("POST", "/api/blog_posts/render_preview", jsonObj, myOnloadFunction);
}
// function that gets called by clicking the button with id="updatePreview_button"
function updatePreview() {
    var markdown = document.getElementById("markdown");
    var jsonObj = {};
    jsonObj["content"] = markdown.value;
    if (!markdown.value.trim()) {
        alert(errorMessageNoMarkdownEntered);
        return;
    }
    function myOnloadFunction(response) {
        if (response == null) {
            alert(errorMessageCommunicationWithServer);
            return;
        }
        else if (response.success) {
            document.getElementById("markdown_preview").innerHTML = response.html;
        }
        else {
            alert(errorMessageUpdatingPreview);
        }
    }
    frontendHelper.makeHttpRequest("POST", "/api/blog_posts/render_preview", jsonObj, myOnloadFunction);
}
// function that gets called as the timer interrupt event
function updateLivePreview() {
    var markdown = document.getElementById("markdown");
    if (!markdown.value.trim()) {
        return; // if the markdown is only containing whitespaces, dont send a request to the server
    }
    var jsonObj = {};
    jsonObj["content"] = markdown.value;
    function myOnloadFunction(response) {
        if (response == null) {
            handleErrorResponseDuringLiveMarkdownRendering("Live-Vorschau: " + errorMessageCommunicationWithServer);
            return;
        }
        else if (response.success) {
            document.getElementById("markdown_preview").innerHTML = response.html;
            timer = setInterval(updateLivePreview, 1000); // restart timer if the request for rendering the preview was successfull
        }
        else {
            handleErrorResponseDuringLiveMarkdownRendering(errorMessageUpdatingOrShowingLivePreview);
        }
    }
    clearInterval(timer); // stop the timer as long as the server needs to respond
    frontendHelper.makeHttpRequest("POST", "/api/blog_posts/render_preview", jsonObj, myOnloadFunction);
}
// If the response of the server while rendering the live preview is null or success is false, this function gets called
function handleErrorResponseDuringLiveMarkdownRendering(alertMessage) {
    var checkBox = document.getElementById("livePreviewCheckbox");
    checkBox.checked = false;
    swapShowingLivePreview(checkBox);
    alert(alertMessage);
}
// onclick function of the live preview checkbox
function swapShowingLivePreview(checkBox) {
    document.getElementById("markdown_preview").innerHTML = "";
    if (checkBox.checked) {
        document.getElementById("updatePreview_button").style.display = "none";
        document.getElementById("preview_div").style.display = "block";
        document.getElementById("hidePreview_button").style.display = "none";
        document.getElementById("swapShowingPreview_button").style.display = "none";
        document.getElementById("preview-button-group").style.height = "0";
        scroll(0, 400);
        timer = setInterval(updateLivePreview, 1000);
    }
    else {
        clearInterval(timer);
        document.getElementById("preview_div").style.display = "none";
        document.getElementById("swapShowingPreview_button").style.display = "block";
        document.getElementById("preview-button-group").style.height = "3vw";
    }
}
function saveCreatedBlogPost() {
    var title = document.getElementById("title");
    var markdown = document.getElementById("markdown");
    if (title.value.trim() && markdown.value.trim()) // checking if the strings are containing only whitespaces
     {
        var jsonObj = {};
        jsonObj["title"] = title.value;
        jsonObj["content"] = markdown.value;
        function myOnloadFunction(response) {
            if (response == null) {
                alert(errorMessageCommunicationWithServer);
                return;
            }
            else if (response.success) {
                window.location.href = "/#"; //TODO: Link to the blog post overview of all post
            }
            else {
                alert(errorMessageSaving + "\n➔ " + response.errors[0].title + ".");
            }
        }
        frontendHelper.makeHttpRequest("POST", "/api/blog_posts", jsonObj, myOnloadFunction);
    }
    else {
        title.value = title.value.trim();
        markdown.value = markdown.value.trim();
    }
}
function saveEditedBlogPost() {
    var title = document.getElementById("title");
    var markdown = document.getElementById("markdown");
    if (title.value.trim() && markdown.value.trim()) // Checking if the strings are containing only whitespaces
     {
        var jsonObj = {};
        jsonObj["id"] = document.getElementById("id").innerHTML;
        jsonObj["title"] = title.value;
        jsonObj["content"] = markdown.value;
        function myOnloadFunction(response) {
            if (response == null) {
                alert(errorMessageCommunicationWithServer);
                return;
            }
            else if (response.success) {
                window.location.href = "/#"; //TODO: Link to the blog post overview of all post
            }
            else {
                alert(errorMessageSaving + "\n➔ " + response.errors[0].title + ".");
            }
        }
        frontendHelper.makeHttpRequest("PUT", "/api/blog_posts/update", jsonObj, myOnloadFunction);
    }
    else {
        title.value = title.value.trim();
        markdown.value = markdown.value.trim();
    }
}
function cancelCreatingOrEditing(alertMessage) {
    var wantsToCancel = confirm(alertMessage);
    if (wantsToCancel) {
        window.history.back();
    }
}
