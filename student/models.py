from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Student(models.Model):
      rollno = models.CharField(max_length=10,unique=True)
      name = models.CharField(max_length=30)
      dept = models.CharField(max_length=10)
      email = models.CharField(max_length=100)
      address = models.CharField(max_length=180)
      aboutme = models.TextField()
      passcode = models.CharField(max_length=10)
