from vereinswebseite.models.blog_post import BlogPost


def can_user_edit_blog_post(user, post: BlogPost) -> bool:
    if not user.is_authenticated:
        return False
    return has_role(user, "Webmaster") or post.author_id == user.id


def can_user_delete_blog_post(user, post: BlogPost) -> bool:
    if not user.is_authenticated:
        return False
    return has_role(user, "Webmaster") or post.author_id == user.id


def has_role(user, role: str) -> bool:
    roles = [role.name for role in user.roles]
    return role in roles
