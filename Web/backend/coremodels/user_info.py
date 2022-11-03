from django.db import models
from django.contrib.auth.models import User
from backend.coremodels.cost_center import CostCenter
from django.contrib.auth.models import Group


# This class is used to extend the already existing User class in Django.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='test')
    cost_center = models.ForeignKey(
        CostCenter,  on_delete=models.CASCADE, null=True)
    # group points to the built-in django class Group,
    # which works as the intended "role" in the database schema
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
