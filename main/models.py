from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)


class Job(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)


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

