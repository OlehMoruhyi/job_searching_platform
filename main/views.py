from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Offer, Seeker, Employer, CV, OfferResponse, CVResponse
from .forms import SeekerRegistrationForm, EmployerRegistrationForm, LoginForm, SeekerForm, EmployerForm, OfferForm, \
    CVForm


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


class ResponseView(LoginRequiredMixin, View):  # Serhii

    def get(self, request, pk):
        user = request.user
        if hasattr(user, 'seeker'):
            cv = CV.objects.get(pk=pk)
            offers = cv.offers.all()

            template_name = "main/cv_response.html"
            context = {'offers': offers, 'cv': cv}

        elif hasattr(user, 'employer'):
            offer = Offer.objects.get(pk=pk)
            cvs = offer.cvs.all()

            template_name = "main/offer_response.html"
            context = {'cvs': cvs, 'offer': offer}
        else:
            raise Http404

        return render(request=request, template_name=template_name, context=context)


class HomeView(View):  # Oleh
    template_name = 'index.html'

    def get(self, request):
        is_employee = hasattr(request.user, 'employer')
        recent = Offer.objects.all()[:8]
        spotlight = Offer.objects.all()[:3]
        return render(request, 'main/index.html', {'recent': recent, 'spotlight': spotlight, 'is_employee': is_employee})


class OfferListView(View):  # Oleh
    def get(self, request):
        if hasattr(request.user, 'employer'):
            return redirect('home')
        name = request.GET.get("name", default="")
        location = request.GET.get("location", default="")
        check_rate = request.GET.get("check_rate", default="check-6")
        check_type = request.GET.get("check_type", default="check-1")

        recent = Offer.objects.filter(name__icontains=name, location__name__icontains=location)
        match check_type:
            case "check-2":
                recent = recent.filter(is_full_time=True)
            case "check-3":
                recent = recent.filter(is_part_time=True)

        match check_rate:
            case "check-7":
                recent = recent.filter(salary_min__range=[0, 25])
            case "check-8":
                recent = recent.filter(salary_min__range=[25, 50])
            case "check-9":
                recent = recent.filter(salary_min__range=[50, 100])
            case "check-10":
                recent = recent.filter(salary_min__range=[100, 200])
            case "check-11":
                recent = recent.filter(salary_min__gte=200)

        paginator = Paginator(recent, 15)
        page_number = request.GET.get("page", default=1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'main/dashboard_offers.html', {"page_obj": page_obj, 'find_name': name,
                                                              'find_location': location, 'find_type': check_type,
                                                              'find_rate': check_rate})


class OfferDetailView(DetailView):  # Yehor
    model = Offer
    template_name = 'main/job-page.html'
    slug_url_kwarg = 'pk'
    context_object_name = 'offer'


class OfferCreateView(CreateView):  # Yehor
    form_class = OfferForm
    template_name = 'main/add-job.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        employer = Employer.objects.get(user=user)
        form.instance.employer = employer
        form.save()
        messages.success(self.request, "The task was created successfully.")
        return super(OfferCreateView, self).form_valid(form)


class OfferUpdateView(UpdateView):  # Yehor
    model = Offer
    form_class = OfferForm
    slug_url_kwarg = 'pk'
    template_name = 'main/update-job.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The task was created successfully.")
        return super(OfferUpdateView, self).form_valid(form)


class OfferDeleteView(DeleteView):  # Oleh
    model = Offer
    context_object_name = 'offer'
    success_url = reverse_lazy('home')
    template_name = 'main/offer_delete.html'

    def form_valid(self, form):
        messages.success(self.request, "The task was deleted successfully.")
        return super(OfferDeleteView, self).form_valid(form)


class CVListView(View):  # Lesha
    # specify the model for list view
    model = CV
    template_name = 'main/cv-list.html'
    context_object_name = 'cvs'

    def get(self, request):
        if not hasattr(request.user, 'employer'):
            return redirect('home')
        name = request.GET.get("name", default="")
        location = request.GET.get("location", default="")
        check_rate = request.GET.get("check_rate", default="check-6")

        recent = CV.objects.filter(seeker__name__icontains=name, location__name__icontains=location)

        match check_rate:
            case "check-7":
                recent = recent.filter(salary__range=[0, 25])
            case "check-8":
                recent = recent.filter(salary__range=[25, 50])
            case "check-9":
                recent = recent.filter(salary__range=[50, 100])
            case "check-10":
                recent = recent.filter(salary__range=[100, 200])
            case "check-11":
                recent = recent.filter(salary__gte=200)

        paginator = Paginator(recent, 15)
        page_number = request.GET.get("page", default=1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'main/cv-list.html', {"page_obj": page_obj, 'find_name': name,
                                                              'find_location': location,
                                                              'find_rate': check_rate})


class CVDetailView(DetailView):  # Lesha
    model = CV
    template_name = 'main/cv-detail.html'
    slug_url_kwarg = 'pk'
    # context_object_name = 'cv'


class CVCreateView(CreateView):  # Lesha
    form_class = CVForm
    template_name = 'main/add-cv.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        seeker = Seeker.objects.get(user=user)
        form.instance.seeker = seeker
        form.save()
        messages.success(self.request, "The cv was created successfully.")
        return super(CVCreateView, self).form_valid(form)


class CVUpdateView(UpdateView):  # Lesha
    model = CV
    form_class = CVForm
    slug_url_kwarg = 'pk'
    template_name = 'main/update-cv.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The cv was Updated successfully.")
        return super(CVUpdateView, self).form_valid(form)


class CVDeleteView(DeleteView):  # Lesha
    model = CV
    context_object_name = 'cv'
    success_url = reverse_lazy("cv-list")

    def form_valid(self, form):
        messages.success(self.request, "The CV was deleted successfully.")
        return super(CVDeleteView, self).form_valid(form)


class SendCVView(View):  # Oleh
    def get(self, request, pk):
        return redirect(f'/dashboard/offer/{pk}')

    def post(self, request, pk):
        cover_letter = request.POST.get("cover_letter", default="")
        cv_id = request.POST.get("cv_id", default="")
        offer_response = OfferResponse(offer=Offer.objects.get(pk=pk), cv=CV.objects.get(pk=cv_id), letter=cover_letter)
        offer_response.save()

        return redirect(f'/dashboard/offer/{pk}')


class SendOfferView(View):  # Oleh
    def get(self, request, pk):
        return redirect(f'/dashboard/cv/{pk}')

    def post(self, request, pk):
        cover_letter = request.POST.get("cover_letter", default="")
        offer_id = request.POST.get("offer_id", default="")
        cv_response = CVResponse(offer=Offer.objects.get(pk=offer_id), cv=CV.objects.get(pk=pk), letter=cover_letter)
        cv_response.save()

        return redirect(f'/dashboard/cv/{pk}')
