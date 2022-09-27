from django.db import models
from django.contrib.auth.models import


class User(models.Model):
    username = models.CharField(max_length=30)
    password_id = models.CharField(max_length=30)
    cost_center = models.CharField(max_length=30)
    roles =
