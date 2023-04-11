from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(template_name='main/index.html'), name='home'),

    path("accounts/registration", views.registration_request, name='registration'),
    path("accounts/seeker_registration", views.seeker_registration_request, name='seeker_registration'),
    path("accounts/employer_registration", views.employer_registration_request, name='employer_registration'),

    path("accounts/login", views.login_request, name='login'),
    path("accounts/logout", auth_views.LogoutView.as_view(), name='logout'),
    path("accounts/password_change", views.PasswordChangeView.as_view(), name='password_change'),

    path("accounts/profile", views.ProfileView.as_view(), name='profile'),
    path("accounts/profile/update", views.profile_update, name='profile_update'),

    path("dashboard/offer", views.OfferListView.as_view(), name='dash'),
    path("dashboard/offer/<pk>", views.OfferDetailView.as_view(), name='offer'),
    path("dashboard/offer/<pk>/send", views.SendCVView.as_view(), name='send_offer'),

    path("dashboard/cv", views.CVListView.as_view(), name='cv_dash'),
    path("dashboard/cv/<pk>", views.CVDetailView.as_view(), name='cv'),

    path("accounts/profile/offer", views.ProfileOfferListView.as_view(), name='offers'),

    path("accounts/profile/offer/<pk>", views.OfferDetailView.as_view(), name='offer_detail'),
    path("accounts/profile/offer/create", views.OfferCreateView.as_view(), name='offer_create'),
    path("accounts/profile/offer/<pk>/update", views.OfferUpdateView.as_view(), name='offer_update'),
    path("accounts/profile/offer/<pk>/delete", views.OfferDeleteView.as_view(), name='offer_delete'),
]
