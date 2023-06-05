from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator

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
    salary_min = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    salary_max = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    experience_min = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    experience_max = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    is_part_time = models.BooleanField()
    is_full_time = models.BooleanField()
    is_remotable = models.BooleanField()
    is_in_office = models.BooleanField()
    contact_number = PhoneNumberField()

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    cvs = models.ManyToManyField('CV', through='OfferResponse')

    def __str__(self):
        return self.name


class OfferResponse(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='offer_response')
    letter = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["offer","cv"]


class CVResponse(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='cv_response')
    letter = models.TextField(blank=True, null=True)
    class Meta:
        unique_together = ["offer","cv"]
