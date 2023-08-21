from django import template

register = template.Library()


@register.filter()
def media_path(blog):
    if blog:
        return f'/media/{blog}'
    return '/static/blog.png'