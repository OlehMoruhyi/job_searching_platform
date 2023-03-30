from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import View
from .models import User, Offer

from .forms import NewUserForm


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        recent = Offer.objects.all()
        spotlight = Offer.objects.all()
        return render(request, 'main/index.html', {'recent': recent, 'spotlight': spotlight})


class ProfileView(View):  # Serhii
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



