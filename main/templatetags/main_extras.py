from django import template

from django.contrib.auth.models import User

register = template.Library()


def user_type(user: User) -> str | None:
    if user.is_authenticated:
        if hasattr(user, 'seeker'):
            return 'seeker'
        if hasattr(user, 'employer'):
            return 'employer'

    return None


register.filter("type", user_type)
