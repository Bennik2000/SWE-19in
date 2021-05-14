var frontendHelper = new FrontendHelper();
var isShowingPreview = false;
var lastRenderedMarkdown;
var timer;
var errorMessageCommunicationWithServer = "Kommunikation mit Server fehlgeschlagen!";
var errorMessageSaving = "Speichern fehlgeschlagen!";
var errorMessageNoMarkdownEntered = "Um eine Vorschau anzeigen zu lassen bitte Markdown angeben!";
var errorMessageShowingPreview = "Anzeigen der Vorschau fehlgeschlagen!";
var errorMessageUpdatingPreview = "Aktualisieren der Vorschau fehlgeschlagen!";
var errorMessageUpdatingOrShowingLivePreview = "Live-Vorschau: Anzeigen/Aktualisieren fehlgeschlagen!";
var errorMessageNoFilesSelected = "Bitte Bild zum Hochladen auswählen!";
var errorMessageUploadingFiles = "Hochladen fehlgeschlagen!";
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
        document.getElementById("markdown_preview").innerHTML = "";
        return; // if the markdown is only containing whitespaces, dont send a request to the server
    }
    if (lastRenderedMarkdown == markdown.value) {
        return; // if the user didnt change the markdown, dont send a request to the server
    }
    var jsonObj = {};
    jsonObj["content"] = markdown.value;
    function myOnloadFunction(response) {
        if (response == null) {
            handleErrorResponseDuringLiveMarkdownRendering("Live-Vorschau: " + errorMessageCommunicationWithServer);
            return;
        }
        else if (response.success) {
            lastRenderedMarkdown = markdown.value;
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
        lastRenderedMarkdown = "";
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
    var expiration_date = document.getElementById("datePicker");
    if (title.value.trim() && markdown.value.trim()) // checking if the strings are containing only whitespaces
     {
        var jsonObj = {};
        jsonObj["title"] = title.value;
        jsonObj["content"] = markdown.value;
        if (expiration_date.value.length > 0) {
            jsonObj["expiration_date"] = expiration_date.value;
        }
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
    var expiration_date = document.getElementById("datePicker");
    if (title.value.trim() && markdown.value.trim()) // Checking if the strings are containing only whitespaces
     {
        var jsonObj = {};
        jsonObj["id"] = document.getElementById("id").innerHTML;
        jsonObj["title"] = title.value;
        jsonObj["content"] = markdown.value;
        if (expiration_date.value.length > 0) {
            jsonObj["expiration_date"] = expiration_date.value;
        }
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
function getCurrentDate() {
    var date = new Date();
    var minimum = document.getElementById("datePicker");
    var month = (date.getMonth() + 1).toString();
    var day = (date.getDate()).toString();
    if (month.length < 2) {
        month = "0" + month;
    }
    if (day.length < 2) {
        day = "0" + day;
    }
    var currentDate = date.getFullYear() + "-" + month + "-" + day;
    minimum.setAttribute("min", currentDate);
}
function setExpirationDate() {
    var minimum = document.getElementById("datePicker");
    var currentExpirationDate = document.getElementById("expiration_date").innerHTML;
    currentExpirationDate = currentExpirationDate.substring(0, 10);
    minimum.setAttribute("value", currentExpirationDate);
}
function uploadImage() {
    var filesInput = document.getElementById("filesInput");
    if (filesInput.files.length == 0) {
        alert(errorMessageNoFilesSelected);
        return;
    }
    var formData = new FormData();
    formData.append("image", filesInput.files[0], filesInput.files[0].name);
    function myOnloadFunction(response) {
        if (response == null) {
            alert(errorMessageCommunicationWithServer);
            return;
        }
        else if (response.success) {
            var respondedFilename = response.filename;
            embedImageIntoMarkdown(respondedFilename);
        }
        else {
            alert(errorMessageUploadingFiles + "\n➔ " + response.errors[0].title + ".");
        }
    }
    frontendHelper.makeHttpRequest("POST", "/api/upload_image", formData, myOnloadFunction, false);
    filesInput.value = "";
}
function embedImageIntoMarkdown(filename) {
    var markdown = document.getElementById("markdown");
    var imageURL = "![](/_uploads/images/" + filename + "){: style='width: 5vw;'}";
    if (markdown.selectionStart || markdown.selectionStart === 0) {
        var startPos = markdown.selectionStart;
        var endPos = markdown.selectionEnd;
        markdown.value = markdown.value.substring(0, startPos) + imageURL + markdown.value.substring(endPos, markdown.value.length);
        markdown.selectionStart = startPos + imageURL.length;
        markdown.selectionEnd = startPos + imageURL.length;
    }
    else {
        markdown.value += imageURL;
    }
}
function deleteBlogPost() {
    var wantsToCancel = confirm("Soll der Beitrag wirklich gelöscht werden?");
    if (wantsToCancel) {
        var jsonObj = {};
        jsonObj["id"] = document.getElementById("id").innerHTML;
        function myOnloadFunction(response) {
            if (response == null) {
                alert("Kommunikation mit Server fehlgeschlagen!");
                return;
            }
            else if (response.success) {
                alert("Artikel erfolgreich gelöscht!");
                window.location.href = "/#"; //TODO: Link to the blog post overview of all post
            }
            else {
                alert("Löschen fehlgeschlagen!" + "\n➔ " + response.errors[0].title + ".");
            }
        }
        frontendHelper.makeHttpRequest("DELETE", "/api/blog_posts/delete", jsonObj, myOnloadFunction);
    }
}
function changeCheckboxChecked() {
    var checkBox = document.getElementById("livePreviewCheckbox");
    checkBox.checked = !checkBox.checked;
    swapShowingLivePreview(checkBox);
}
