from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Job(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Seeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    birthday = models.DateField(blank=True, null=True)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.seeker.id, filename)


class CV(models.Model):
    location = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, blank=True, null=True)
    is_part_time = models.BooleanField()
    is_full_time = models.BooleanField()
    is_remotable = models.BooleanField()
    is_in_office = models.BooleanField()
    phone_number = PhoneNumberField()
    preferable_job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    salary = models.IntegerField()
    experience = models.IntegerField()
    cv_file = models.FileField(upload_to=user_directory_path, blank=True)

    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    offers = models.ManyToManyField('Offer', through='CVResponse')

    def cv_file_name(self):
        return self.cv_file.name.split('/')[-1]

    def __str__(self):
        return self.preferable_job.name


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)


class Offer(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    location = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    experience_min = models.IntegerField()
    experience_max = models.IntegerField()
    is_part_time = models.BooleanField()
    is_full_time = models.BooleanField()
    is_remotable = models.BooleanField()
    is_in_office = models.BooleanField()
    contact_number = PhoneNumberField()
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OfferResponse(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    is_from_user = models.BooleanField()


class CVResponse(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    letter = models.TextField(blank=True, null=True)
