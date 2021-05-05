var frontendHelper = new FrontendHelper();
function add_post_button() {
    window.location.href = "/account";
}
function post_more_button() {
    window.location.href = "/login";
}
function post_edit_button() {
    window.location.href = "/account";
}
function get_all_blogs() {
    var post_list = document.getElementById("post_list");
    function myOnloadFunction(response) {
        if (response) {
            if (response.success == true) {
                response.blog_posts.forEach(function (post) {
                    function myOnloadFunction(response) {
                        var col = document.createElement("div");
                        col.classList.add("col-md-12");
                        col.classList.add("mb-3");
                        var container = document.createElement("div");
                        container.classList.add("container");
                        container.classList.add("position-relative");
                        container.setAttribute("id", "post");
                        var row = document.createElement("div");
                        row.classList.add("row");
                        var post_titel = document.createElement("h3");
                        post_titel.innerHTML = post.title;
                        post_titel.classList.add("col-sm-12");
                        post_titel.setAttribute("id", "post_titel");
                        var post_meta = document.createElement("div");
                        post_meta.classList.add("col-sm-12");
                        post_meta.classList.add("mb-1");
                        post_meta.setAttribute("id", "post_meta");
                        var post_author = document.createElement("span");
                        post_author.setAttribute("id", "post_author");
                        post_author.innerHTML = post.author;
                        var post_date = document.createElement("span");
                        post_date.setAttribute("id", "post_date");
                        post_date.innerHTML = post.creation_date;
                        var post_separator = document.createElement("hr");
                        var post_content = document.createElement("div");
                        post_content.classList.add("col-md-12");
                        post_content.setAttribute("id", "post_content");
                        post_content.innerHTML = response.html;
                        var post_more = document.createElement("div");
                        post_more.classList.add("col-md-1");
                        post_more.classList.add("btn");
                        post_more.setAttribute("onclick", "post_more_button();");
                        post_more.setAttribute("id", "post_more");
                        post_more.setAttribute("href", "#");
                        post_more.innerHTML = "mehr...";
                        var post_edit = document.createElement("div");
                        post_edit.classList.add("col-md-1");
                        post_edit.classList.add("offset-md-10");
                        post_edit.classList.add("btn");
                        post_edit.classList.add("btn-primary");
                        post_edit.classList.add("pl-2");
                        post_edit.setAttribute("onclick", "post_edit_button();");
                        post_edit.setAttribute("id", "post_edit");
                        post_edit.setAttribute("href", "#");
                        post_edit.innerHTML = "bearbeiten";
                        post_meta.appendChild(post_author);
                        row.appendChild(post_titel);
                        row.appendChild(post_meta);
                        row.appendChild(post_separator);
                        row.appendChild(post_content);
                        row.appendChild(post_more);
                        row.appendChild(post_edit);
                        container.appendChild(row);
                        col.appendChild(container);
                        post_list.appendChild(col);
                    }
                    var jsonObj = {};
                    jsonObj["content"] = post.content;
                    frontendHelper.makeHttpRequest("POST", "/api/blog_posts/render_preview", jsonObj, myOnloadFunction);
                });
            }
            else {
                alert("Server Error while loading Posts!");
            }
        }
        else {
            alert("Server Error!");
        }
    }
    var jsonObj = {};
    frontendHelper.makeHttpRequest("GET", "/api/blog_posts", jsonObj, myOnloadFunction);
}
window.onload = function () {
    get_all_blogs();
};
