from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=('seeker', 'employer'))

    class Meta:
        model = User
        fields = ("email", "user_type", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data['user_type'] == 'seeker':
            user.seeker = None
        else:
            user.employer = None

        if commit:
            user.save()
        return user
