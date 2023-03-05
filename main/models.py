from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=50)
    is_seeker = models.BooleanField()


class Seeker(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)  # \\TO_REWORK
    commitment = models.BooleanField
    is_remotable = models.BooleanField
    birthday = models.DateField()
    phone_number = PhoneNumberField()
    preferable_job = models.CharField(max_length=100)  # ADD a foreign key \\TO_REWORK
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    experience = models.IntegerField()
    CV = models.FileField()


class Employer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    contact_number = PhoneNumberField()


class OfferResponse(models.Model):
    offer_id = models.CharField(max_length=100)  # \\TO_REWORK
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    is_from_user = models.BooleanField()
