# from unittest.util import _MAX_LENGTH
from django.db import models
from backend.coremodels.cost_center import CostCenter


class StorageUnit(models.Model):
    '''A unit containing several compartments.'''
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=30)
    building = models.CharField(max_length=30)
    floor = models.CharField(max_length=30)
    cost_center = models.ForeignKey(
        CostCenter,  on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
