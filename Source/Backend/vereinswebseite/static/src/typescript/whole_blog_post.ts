let frontendHelper = new FrontendHelper()

function bodyOnload() {
    var contentDiv = document.getElementById("content");

    if(contentDiv.scrollHeight > contentDiv.clientHeight || contentDiv.getBoundingClientRect().bottom > (window.innerHeight || contentDiv.clientHeight )){
        document.getElementById("button_scrollToBottom").style.display = "block";
        document.getElementById("button_scrollToTop").style.display = "inline-flex";
    }
}

function editBlogPost() {
    let id = document.getElementById("id").innerHTML;
    window.location.href = "/blog_posts/edit?post_id="+ id;
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

function scrollToContent(direction: String) {
    if (direction == "bottom") {
        document.getElementById("content").scrollIntoView(false);
    }
    else {
        document.getElementById("content").scrollIntoView();
    }
}
