from vereinswebseite.models.blog_post import BlogPost


def can_user_edit_blog_post(user, post: BlogPost) -> bool:
    if not user.is_authenticated:
        return False
    return _is_webmaster(user) or post.author_id == user.id


def can_user_delete_blog_post(user, post: BlogPost) -> bool:
    if not user.is_authenticated:
        return False
    return _is_webmaster(user) or post.author_id == user.id


def _is_webmaster(user) -> bool:
    return user.has_roles("Webmaster")
