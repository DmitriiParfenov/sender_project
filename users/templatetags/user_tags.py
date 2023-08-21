from django import template

register = template.Library()


@register.filter()
def media_path(user):
    if user:
        return f'/media/{user}'
    return '/static/sample.png'