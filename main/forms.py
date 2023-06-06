from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Offer, Seeker, Employer, CV
from cities_light.models import City
from phonenumber_field.formfields import PhoneNumberField

from .models import Seeker, Employer
class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email)
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists")
        return email

    def save(self, commit=True):
        profile = super(UserRegistrationForm, self).save(commit=False)
        try:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'])
            profile.user = user
            if commit:
                user.save()
                profile.save()
            return profile
        except IntegrityError as e:
            raise ValidationError(e)


class SeekerForm(forms.ModelForm):
    class Meta:
        model = Seeker
        fields = ('name', 'surname', 'last_name', 'birthday')

    name = forms.CharField()
    surname = forms.CharField()
    last_name = forms.CharField(required=False, label_suffix=' (optional):')
    birthday = forms.DateField(widget=forms.DateInput, required=False)


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company_name',)

    company_name = forms.CharField()


class SeekerRegistrationForm(UserRegistrationForm, SeekerForm):
    field_order = ('email', 'name', 'surname', 'last_name', 'birthday', 'password')


class EmployerRegistrationForm(UserRegistrationForm, EmployerForm):
    field_order = ('email', 'company_name', 'password')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class OfferForm(forms.ModelForm):
    salary_min = forms.IntegerField(min_value=0)
    salary_max = forms.IntegerField(min_value=1)
    experience_min = forms.IntegerField(min_value=0)
    experience_max = forms.IntegerField(min_value=1)


    class Meta:
        model = Offer
        #exclude = ('Employer',)
        fields = ('name', 'description', 'location', 'job', 'salary_min','salary_max','experience_min','experience_max','is_part_time','is_full_time','is_remotable','is_in_office','contact_number')

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get("salary_min")
        salary_max = cleaned_data.get("salary_max")
        experience_min = cleaned_data.get("experience_min")
        experience_max = cleaned_data.get("experience_max")

        if salary_min and salary_max:
            # Only do something if both fields are valid so far.
            if salary_min > salary_max:
                raise forms.ValidationError(
                    "Food min. has to be less then Food max."
                )
        if experience_min and experience_max:
            # Only do something if both fields are valid so far.
            if experience_min > experience_max:
                raise forms.ValidationError(
                    "Food min. has to be less then Food max."
                )

        
class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ('location', 'is_part_time','is_full_time','is_remotable','is_in_office','phone_number','preferable_job', 'salary', 'experience', 'cv_file')

       
