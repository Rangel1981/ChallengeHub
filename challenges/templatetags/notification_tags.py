from django import template

register = template.Library()

@register.filter
def unread_count(user):
    if user.is_authenticated:
        return user.notifications.filter(is_read=False).count()
    return 0
