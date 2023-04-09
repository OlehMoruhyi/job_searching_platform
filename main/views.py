from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, Http404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy

from .models import Offer, Seeker
from .forms import SeekerRegistrationForm, EmployerRegistrationForm, LoginForm


def registration_request(request):
    return render(request=request, template_name="registration/registration.html", context={'title': 'Registration'})


def user_registration_request(request, form_class):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            user_obj = form.save()
            login(request, user_obj.user)
            return redirect(request.GET.get('next', reverse_lazy('home')))
    else:
        form = form_class()
    return render(request=request, template_name="form.html", context={"form": form, 'title': 'Registration'})


def seeker_registration_request(request):
    return user_registration_request(request, SeekerRegistrationForm)


def employer_registration_request(request):
    return user_registration_request(request, EmployerRegistrationForm)


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect(request.GET['next'])
            form.add_error(None, 'User doas not exist')
    else:
        form = LoginForm()
    return render(request=request, template_name="form.html", context={"form": form, 'title': 'Log In'})
    # return render(request=request, template_name="registration/login.html", context={"form": form})


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        recent = Offer.objects.all()
        spotlight = Offer.objects.all()
        return render(request, 'main/index.html', {'recent': recent, 'spotlight': spotlight})


class ProfileView(LoginRequiredMixin, View):  # Serhii
    ...


class OfferListView(View):  # Lesha
    ...


class OfferDetailView(View):  # Yehor
    ...


class SendCVView(View):  # Lesha
    ...


class CVListView(View):  # Lesha
    ...


class CVDetailView(View):  # Yehor
    ...


class ProfileOfferListView(View):  # Oleh
    ...


class OfferCreateView(View):  # Oleh, Serhii
    ...


class OfferUpdateView(View):  # Oleh, Serhii
    ...


class OfferDeleteView(View):  # Oleh, Serhii
    ...
