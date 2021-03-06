var frontendHelper = new FrontendHelper();
window.addEventListener('resize', showOrHideScrollButtons);
function showOrHideScrollButtons() {
    var contentDiv = document.getElementById("content");
    if (contentDiv.scrollHeight > contentDiv.clientHeight || contentDiv.getBoundingClientRect().bottom > (window.innerHeight || contentDiv.clientHeight)) {
        document.getElementById("button_scrollToBottom").style.display = "block";
        document.getElementById("button_scrollToTop").style.display = "inline-flex";
    }
    else {
        document.getElementById("button_scrollToBottom").style.display = "none";
        document.getElementById("button_scrollToTop").style.display = "none";
    }
}
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
                window.location.href = "/blog_posts/all";
            }
            else {
                alert("Löschen fehlgeschlagen!" + "\n➔ " + response.errors[0].title + ".");
            }
        }
        frontendHelper.makeHttpRequest("DELETE", "/api/blog_posts/delete", jsonObj, myOnloadFunction);
    }
}
function scrollToContent(direction) {
    if (direction == "bottom") {
        document.getElementById("post").scrollIntoView(false);
    }
    else {
        document.getElementById("post").scrollIntoView();
    }
}
document.getElementById("post").addEventListener("resize", function () {
    var post = document.getElementById("post");
    var elHeight = post.offsetHeight;
    elHeight += parseInt(window.getComputedStyle(post).getPropertyValue('margin-top'));
    elHeight += parseInt(window.getComputedStyle(post).getPropertyValue('margin-bottom'));
    elHeight += 1;
    var message = { height: document.getElementById("post").scrollHeight, scroll: false };
    window.parent.postMessage(message, "*");
});
window.onload = function () {
    var post = document.getElementById("post");
    var elHeight = post.offsetHeight;
    elHeight += parseInt(window.getComputedStyle(post).getPropertyValue('margin-top'));
    elHeight += parseInt(window.getComputedStyle(post).getPropertyValue('margin-bottom'));
    elHeight += 1;
    var message = { height: elHeight, scroll: true };
    window.parent.postMessage(message, "*");
};
