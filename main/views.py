from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import View

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
        return render(request, 'main/index.html')


class ProfileView(View):
    ...


class OfferListView(View):
    ...


class OfferDetailView(View):
    ...


class SendCVView(View):
    ...


class CVListView(View):
    ...


class CVDetailView(View):
    ...


class ProfileOfferListView(View):
    ...


class OfferCreateView(View):
    ...


class OfferUpdateView(View):
    ...


class OfferDeleteView(View):
    ...



