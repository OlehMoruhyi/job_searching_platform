from django.contrib import admin
from django.urls import path, include

from . import views

name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(template_name='index.html'), name='home'),
    path("accounts", include("django.contrib.auth.urls")),
    path("accounts/registration", views.register_request, name='registration'),
    path("accounts/profile", views.ProfileView.as_view(), name='profile'),

    path("dashboard/offer", views.OfferListView.as_view(), name='dash'),
    path("dashboard/offer/{id}", views.OfferDetailView.as_view(), name='offer'),
    path("dashboard/offer/{id}/send", views.SendCVView.as_view(), name='profile'),

    path("dashboard/cv", views.CVListView.as_view(), name='cv_dash'),
    path("dashboard/cv/{id}", views.CVDetailView.as_view(), name='cv'),

    path("accounts/profile/offer", views.ProfileOfferListView.as_view(), name='offers'),

    path("accounts/profile/offer/{id}", views.OfferDetailView.as_view(), name='offer_detail'),
    path("accounts/profile/offer/create", views.OfferCreateView.as_view(), name='offer_create'),
    path("accounts/profile/offer/{id}/update", views.OfferUpdateView.as_view(), name='offer_update'),
    path("accounts/profile/offer/{id}/delete", views.OfferDeleteView.as_view(), name='offer_delete'),
]
