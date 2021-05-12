var frontendHelper = new FrontendHelper();
function add_post_button() {
    window.location.href = "/blog_posts/create";
}
function post_more_button(id) {
    window.location.href = "/blog_posts/render?post_id=" + id;
}
function post_edit_button(id) {
    window.location.href = "/blog_posts/edit?post_id=" + id;
}
