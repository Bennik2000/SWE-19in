let frontendHelper = new FrontendHelper()

function editBlogPost() {
    let id = document.getElementById("id").innerHTML.toString();
    window.location.href = "/blog_posts/edit?posts_id="+ id;
}

function deleteBlogPost() {
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
        frontendHelper.makeHttpRequest("DELETE", "/blog_posts/delete", jsonObj, myOnloadFunction); 
}