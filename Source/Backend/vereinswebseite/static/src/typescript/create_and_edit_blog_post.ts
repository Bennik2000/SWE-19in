let frontendHelper = new FrontendHelper()
var isShowingPreview: Boolean = false;
var lastRenderedMarkdown;
var timer;

let errorMessageCommunicationWithServer = "Kommunikation mit Server fehlgeschlagen!";
let errorMessageSaving = "Speichern fehlgeschlagen!";
let errorMessageNoMarkdownEntered = "Um eine Vorschau anzeigen zu lassen bitte Markdown angeben!";
let errorMessageShowingPreview = "Anzeigen der Vorschau fehlgeschlagen!";
let errorMessageUpdatingPreview = "Aktualisieren der Vorschau fehlgeschlagen!";
let errorMessageUpdatingOrShowingLivePreview = "Live-Vorschau: Anzeigen/Aktualisieren fehlgeschlagen!";
let errorMessageNoFilesSelected = "Bitte Bilder zum Hochladen auswählen!";
let errorMessageUploadingFiles = "Hochladen fehlgeschlagen!";

window.addEventListener('resize', handleZoomEvent);


function swapShowingPreview() {
    var markdown = document.getElementById("markdown") as HTMLInputElement;
    if(isShowingPreview) {
        document.getElementById("markdown_preview").innerHTML = "";
        document.getElementById("updatePreview_button").style.display = "none";     
        document.getElementById("preview_div").style.display = "none";
        document.getElementById("hidePreview_button").style.display = "none";  
        document.getElementById("swapShowingPreview_button").style.display = "block";         
        isShowingPreview = false;   
        return;
    } 

    if(!markdown.value.trim()) {  // Check if the markdown is only containing whitespaces
        alert(errorMessageNoMarkdownEntered);
        return;
    }
    
    var jsonObj = {};
        jsonObj["content"] = markdown.value;

    function myOnloadFunction(response) {
        if(response == null) {
            alert(errorMessageCommunicationWithServer);
            return;
        }
        else if (response.success)
        {
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
    var markdown = document.getElementById("markdown") as HTMLInputElement;
    var jsonObj = {};
        jsonObj["content"] = markdown.value;

    if(!markdown.value.trim()) {
        alert(errorMessageNoMarkdownEntered);
        return;
    }

    function myOnloadFunction(response) {
        if(response == null) {
            alert(errorMessageCommunicationWithServer);
            return
        }
        else if (response.success)
        {
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
    var markdown = document.getElementById("markdown") as HTMLInputElement;
    if(!markdown.value.trim()) {
        document.getElementById("markdown_preview").innerHTML = "";
        return;  // if the markdown is only containing whitespaces, dont send a request to the server
    }

    if(lastRenderedMarkdown == markdown.value)
    {
        return;     // if the user didnt change the markdown, dont send a request to the server
    }

    var jsonObj = {};
        jsonObj["content"] = markdown.value;


    function myOnloadFunction(response) {
        if(response == null) {
            handleErrorResponseDuringLiveMarkdownRendering("Live-Vorschau: " + errorMessageCommunicationWithServer);
            return;
        }
        else if (response.success)
        {
            lastRenderedMarkdown = markdown.value;
            document.getElementById("markdown_preview").innerHTML = response.html;
            timer = setInterval(updateLivePreview, 1000);  // restart timer if the request for rendering the preview was successfull
        }
        else {
            handleErrorResponseDuringLiveMarkdownRendering(errorMessageUpdatingOrShowingLivePreview);
        }
    }
    clearInterval(timer);   // stop the timer as long as the server needs to respond
    frontendHelper.makeHttpRequest("POST", "/api/blog_posts/render_preview", jsonObj, myOnloadFunction);
}

// If the response of the server while rendering the live preview is null or success is false, this function gets called
function handleErrorResponseDuringLiveMarkdownRendering(alertMessage) {
    var checkBox = document.getElementById("livePreviewCheckbox") as HTMLInputElement;
    checkBox.checked = false;
    swapShowingLivePreview(checkBox);
    alert(alertMessage);
}

// onclick function of the live preview checkbox
function swapShowingLivePreview(checkBox) {
    document.getElementById("markdown_preview").innerHTML = "";
    
    if(checkBox.checked) {
        document.getElementById("updatePreview_button").style.display = "none";     
        document.getElementById("preview_div").style.display = "block";
        document.getElementById("hidePreview_button").style.display = "none";  
        document.getElementById("swapShowingPreview_button").style.display = "none";  
        document.getElementById("preview-button-group").style.height = "0";
        lastRenderedMarkdown = "";
        scroll(0,400);
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
    var title = document.getElementById("title") as HTMLInputElement;
    var markdown = document.getElementById("markdown") as HTMLInputElement;
    var expiration_date = document.getElementById("datePicker") as HTMLInputElement;
    
    if (title.value.trim() && markdown.value.trim()) // checking if the strings are containing only whitespaces
    {
        var jsonObj = {};
        jsonObj["title"] = title.value;
        jsonObj["content"] = markdown.value;
        
        if(expiration_date.value.length > 0){
            jsonObj["expiration_date"] = expiration_date.value;
        }
        function myOnloadFunction(response) {
            if(response == null)
            {
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
    var title = document.getElementById("title") as HTMLInputElement;
    var markdown = document.getElementById("markdown") as HTMLInputElement;
    var expiration_date = document.getElementById("datePicker") as HTMLInputElement;
    
    if (title.value.trim() && markdown.value.trim()) // Checking if the strings are containing only whitespaces
    {
        var jsonObj = {};
        jsonObj["id"] = document.getElementById("id").innerHTML;
        jsonObj["title"] = title.value;
        jsonObj["content"] = markdown.value;
        if(expiration_date.value.length > 0){
            jsonObj["expiration_date"] = expiration_date.value;
        }

        function myOnloadFunction(response) {
            if(response == null)
            {
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
    let wantsToCancel = confirm(alertMessage);
    if (wantsToCancel) 
    {
        window.history.back();
    }
}

function getCurrentDate() {
    var date = new Date();
    var minimum = document.getElementById("datePicker");
    var month =(date.getMonth()+1).toString();
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
    currentExpirationDate = currentExpirationDate.substring(0,10);
    minimum.setAttribute("value", currentExpirationDate);
}


function uploadImage() {
    let filesInput = document.getElementById("filesInput") as HTMLInputElement;
 
    if (filesInput.files.length == 0) {
        alert(errorMessageNoFilesSelected);
        return;
    }

    var formData = new FormData();
    formData.append("image", filesInput.files[0], filesInput.files[0].name);

    function myOnloadFunction(response) {
        if(response == null)
        {
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
    let markdown = document.getElementById("markdown") as HTMLInputElement;

    var imageURL = "![](/_uploads/images/" + filename + "){: style='width: 5vw;'}";

    if (markdown.selectionStart || markdown.selectionStart === 0) {
        var startPos = markdown.selectionStart;
        var endPos = markdown.selectionEnd;
        markdown.value = markdown.value.substring(0, startPos) + imageURL + markdown.value.substring(endPos, markdown.value.length);
        markdown.selectionStart = startPos + imageURL.length;
        markdown.selectionEnd = startPos + imageURL.length;
      } else {
        markdown.value += imageURL;
      }
}

function deleteBlogPost() {

    let wantsToCancel = confirm("Soll der Beitrag wirklich gelöscht werden?");
    if (wantsToCancel) 
    {
        var jsonObj = {};
        jsonObj["id"] = document.getElementById("id").innerHTML;

        function myOnloadFunction(response) {
            if(response == null)
            {
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

function handleZoomEvent() {
    var browserZoomLevel = Math.round(((( window.outerWidth - 10 ) / window.innerWidth) * 100));
    switch (browserZoomLevel) {
        case 200: 
            document.body.style.zoom = "180%";
            break;
        case 175: 
            document.body.style.zoom = "155%";
            break;
        case 150: 
            document.body.style.zoom = "130%";
            break;
        case 125: 
            document.body.style.zoom = "105%";
            break;
        case 110: 
            document.body.style.zoom = "90%";
            break;
        case 100: 
            document.body.style.zoom = "80%";
            break;
        case 90:
            document.body.style.zoom = "70%";   
            document.getElementById("livePreviewCheckbox").style.transform = "scale(1.2)";
            break;
        case 80: 
            document.body.style.zoom= "60%";
            document.getElementById("livePreviewCheckbox").style.transform = "scale(1.8)";
            break; 
        case 75: 
            document.body.style.zoom= "55%";
            break;
        case 67: 
            document.body.style.zoom= "47%";
            break;
        case 50: 
            document.body.style.zoom= "40%";
            break;
        case 33: 
            document.body.style.zoom= "23%";
            break;
        case 25: 
            document.body.style.zoom= "15%";
            break;
        default: 
            break;
    }
}