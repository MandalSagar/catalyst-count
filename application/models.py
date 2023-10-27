from django.db import models

# Create your models here.

# class Users(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)

class Data(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = models.PositiveIntegerField(null=True, blank=True)
    industry = models.CharField(max_length=255)
    size_range = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    linkedin_url = models.URLField(max_length=255)
    current_employee_estimate = models.PositiveIntegerField(null=True, blank=True)
    total_employee_estimate = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
