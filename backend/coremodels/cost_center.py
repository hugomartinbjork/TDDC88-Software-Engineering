from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class CostCenter(models.Model):
    name = models.CharField(max_length=30)
    id = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name
