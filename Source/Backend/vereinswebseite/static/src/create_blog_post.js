var isShowingPreview = false;
function swapShowingPreview() {
    var markdown = document.getElementById("markdown");
    if (!isShowingPreview && markdown.value != "") {
        document.getElementById("markdown_preview").innerHTML =
            marked(markdown.value);
        document.getElementById("swapShowingPreview_button").innerHTML = "Vorschau ausblenden";
        isShowingPreview = true;
    }
    else {
        document.getElementById("markdown_preview").innerHTML = "";
        document.getElementById("swapShowingPreview_button").innerHTML = "Vorschau anzeigen";
        isShowingPreview = false;
    }
}
