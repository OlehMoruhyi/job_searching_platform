from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView

from .models import Seeker, Employer, CV, Offer
from .forms import SeekerRegistrationForm, EmployerRegistrationForm, LoginForm, SeekerForm, EmployerForm


def registration_request(request):
    user_type = request.GET.get('user_type')
    if user_type == 'seeker':
        form_class = SeekerRegistrationForm
    elif user_type == 'employer':
        form_class = EmployerRegistrationForm
    else:
        form_class = None

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            profile = form.save()
            login(request, profile.user)
            return redirect(request.GET.get('next', reverse_lazy('home')))
    elif form_class:
        form = form_class()
    else:
        form = None
    return render(request=request, template_name="registration/registration.html",
                  context={"form": form, 'title': 'Registration'})


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect(request.GET.get('next', reverse_lazy('home')))
            form.add_error(None, 'User doas not exist')
    else:
        form = LoginForm()
    return render(request=request, template_name="form.html", context={"form": form, 'title': 'Log In'})


class PasswordChangeView(AuthPasswordChangeView):
    template_name = 'form.html'

    def get_success_url(self):
        return self.request.GET.get('next', 'profile')


class ProfileView(LoginRequiredMixin, View):  # Serhii

    def get(self, request):
        user = request.user
        if hasattr(user, 'seeker'):
            seeker = Seeker.objects.get(user=user)
            cvs = CV.objects.filter(seeker=seeker)

            template_name = "main/seeker_profile.html"
            context = {'seeker': seeker, 'cvs': cvs, }

        elif hasattr(user, 'employer'):
            employer = Employer.objects.get(user=user)
            offers = Offer.objects.filter(employer=employer)

            template_name = "main/employer_profile.html"
            context = {'employer': employer, 'offers': offers}
        else:
            raise Http404

        return render(request=request, template_name=template_name, context=context)


@login_required
def profile_update(request):
    if hasattr(request.user, 'seeker'):
        model = Seeker
        form_model = SeekerForm
    elif hasattr(request.user, 'employer'):
        model = Employer
        form_model = EmployerForm
    else:
        raise Http404

    profile = get_object_or_404(model, user=request.user)

    if request.method == 'POST':
        form = form_model(request.POST, instance=profile)
        form.user_id = request.user.id
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next', reverse_lazy('profile')))
    else:
        form = form_model(instance=profile)

    return render(request=request, template_name="form.html", context={"form": form, 'title': 'Update Profile'})


class HomeView(View):  # Oleh
    template_name = 'index.html'

    def get(self, request):
        recent = Offer.objects.all()
        spotlight = Offer.objects.all()
        return render(request, 'main/index.html', {'recent': recent, 'spotlight': spotlight})


class OfferListView(View):  # Oleh
    ...


class OfferDetailView(View):  # Yehor
    ...


class OfferCreateView(View):  # Yehor
    ...


class OfferUpdateView(View):  # Yehor
    ...


class OfferDeleteView(View):  # Oleh
    ...


class CVListView(View):  # Lesha
    ...


class CVDetailView(View):  # Lesha
    ...


class CVCreateView(View):  # Lesha
    ...


class CVUpdateView(View):  # Lesha
    ...


class CVDeleteView(View):  # Lesha
    ...


class SendCVView(View):  # Oleh
    ...
