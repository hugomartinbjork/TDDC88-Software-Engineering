from django.db import models
from django.contrib.auth.models import User
from backend.coremodels.cost_center import CostCenter
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rdxSolutionsBackendProject.settings import SALT

# This class is used to extend the already existing User class in Django.


class UserInfo(models.Model):
    '''User model which extends the base django user model.'''
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    barcode_id = models.CharField(max_length=255, null=True, unique=True)
    nfc_id = models.CharField(max_length=256, null=True, unique=True)
    cost_center = models.ManyToManyField(CostCenter)
    # group points to the built-in django class Group,
    # which works as the intended "role" in the database schema
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)

    # Stores barcode and nfc as hashed values in the DB.
    def save(self, **kwargs):
        self.barcode_id = make_password(self.barcode_id, SALT)
        self.nfc_id = make_password(self.nfc_id, SALT)
        super().save(**kwargs)
