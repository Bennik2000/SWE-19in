var frontendHelper = new FrontendHelper();
function editBlogPost() {
    var id = document.getElementById("id").innerHTML;
    window.location.href = "/blog_posts/edit?post_id=" + id;
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
        frontendHelper.makeHttpRequest("DELETE", "/blog_posts/delete", jsonObj, myOnloadFunction);
    }
}
