from django.db import models

# Create your models here.
class Internship(models.Model):
    internship_Title = models.CharField(max_length=30,blank=True)
    internship_Type = models.CharField(max_length=10,blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    stipend = models.IntegerField(default=5000,blank=True)
    eligibility = models.CharField(max_length=30,blank=True)
    organization = models.CharField(max_length=30,blank=True)
    location = models.CharField(max_length=30,blank=True)
    no_Of_Openings = models.IntegerField(blank=True)
    skills = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.internship_Title