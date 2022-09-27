from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cost_center = models.CharField(max_length=30)

    def __str__(self):
        return self.user
