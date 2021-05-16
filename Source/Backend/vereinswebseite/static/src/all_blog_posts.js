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
function reload() {
    window.location.reload(true);
    var message = { height: document.body.scrollHeight, width: document.body.scrollWidth, scroll: false };
    window.top.postMessage(message, "*");
}
window.onload = function () {
    var message = { height: document.body.scrollHeight, width: document.body.scrollWidth, scroll: false };
    window.top.postMessage(message, "*");
};
