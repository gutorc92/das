from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

class Picture(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name = "pictures")
