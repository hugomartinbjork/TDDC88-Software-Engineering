from django.db import models
from django.contrib.auth.models import User
from backend.coremodels.cost_center import CostCenter
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


# This class is used to extend the already existing User class in Django.

class UserInfo(models.Model):
    '''User information.'''
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    cost_center = models.ManyToManyField(CostCenter)
    # group points to the built-in django class Group,
    # which works as the intended "role" in the database schema
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    @receiver(post_save, sender=User)
    def create_user_info(sender, instance, created, **kwargs):
        if created:
            UserInfo.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_info(sender, instance, **kwargs):
        instance.userinfo.save()
