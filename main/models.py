from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(max_length=20)


class Job(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)


class Seeker(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    location = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL)
    is_part_tyme = models.BooleanField()
    is_remotable = models.BooleanField()
    birthday = models.DateField()
    phone_number = PhoneNumberField()
    preferable_job = models.ForeignKey(Job, on_delete=models.SET_NULL)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    experience = models.IntegerField()
    CV = models.FileField()


class Employer(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    contact_number = PhoneNumberField()


class Offer(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    experience_min = models.IntegerField()
    experience_max = models.IntegerField()
    is_part_tyme = models.BooleanField()
    is_remotable = models.BooleanField()
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)


class OfferResponse(models.Model):
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    is_from_user = models.BooleanField()


def is_a(user: User) -> bool:
    return hasattr(user, 'a')
