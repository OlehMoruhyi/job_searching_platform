from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from cities_light.models import City
from phonenumber_field.formfields import PhoneNumberField

from .models import Seeker, Employer


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password1 = self.cleaned_data['password']
        validate_password(password1)
        return password1

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email)
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists")
        return email

    def save(self, commit=True):
        user_obj = super(RegistrationForm, self).save(commit=False)
        try:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'])
            user_obj.user = user
            if commit:
                user.save()
                user_obj.save()
            return user_obj
        except IntegrityError as e:
            raise ValidationError(e)


class SeekerRegistrationForm(RegistrationForm):
    class Meta:
        model = Seeker
        fields = ('name', 'surname', 'last_name', 'birthday')

    name = forms.CharField()
    surname = forms.CharField()
    last_name = forms.CharField(required=False)
    birthday = forms.DateField(widget=forms.DateInput, required=False)


class EmployerRegistrationForm(RegistrationForm):
    class Meta:
        model = Employer
        fields = ('company_name',)

    company_name = forms.CharField()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

