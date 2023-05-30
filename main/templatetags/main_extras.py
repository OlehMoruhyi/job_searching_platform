from django import template

from django.contrib.auth.models import User
from main.models import Offer, CV, CVResponse, OfferResponse

register = template.Library()


def user_type(user: User) -> str | None:
    if user.is_authenticated:
        if hasattr(user, 'seeker'):
            return 'seeker'
        if hasattr(user, 'employer'):
            return 'employer'

    return None


def get_model_response(model: Offer | CV, model2=Offer | CV) -> int | None:
    print('!!!!!!!!!!!!!!!!!!!!!!\n' + str(model) + '!!!!!!!!!!!!!!!!!!!!!\n')
    if isinstance(model, Offer):
        return model.cv_response.get(cv=model2).id
    elif isinstance(model, CV):
        return model.offer_response.get(offer=model2).id

    return None


register.filter("type", user_type)
register.filter("get_response", get_model_response)
