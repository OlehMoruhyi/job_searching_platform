from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError

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
    last_name = forms.CharField(required=False)
    birthday = forms.DateField(widget=forms.DateInput, required=False)


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company_name',)

    company_name = forms.CharField()


class SeekerRegistrationForm(UserRegistrationForm, SeekerForm):
    pass


class EmployerRegistrationForm(UserRegistrationForm, EmployerForm):
    pass


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
