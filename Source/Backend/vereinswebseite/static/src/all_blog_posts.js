var frontendHelper = new FrontendHelper();
function add_post_button() {
    window.open("/blog_posts/create", '_blank');
}
function post_more_button(id) {
    window.location.href = "/blog_posts/render?post_id=" + id;
}
function post_edit_button(id) {
    window.open("/blog_posts/edit?post_id=" + id, '_blank');
}