# from unittest.util import _MAX_LENGTH
from django.db import models
from backend.coremodels.cost_center import CostCenter


class Storage(models.Model):
    '''A unit containing several compartments.'''
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=30)
    building = models.CharField(max_length=30)
    floor = models.CharField(max_length=30)
    cost_center = models.ForeignKey(
        CostCenter,  on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = (("get_storage_cost", "Can see storage cost"),
                       ("get_storage_value", "Can see storage value"),
                       ("return_to_storage", "Can return article to storage"),
                       ("add_input_unit", "Can ad an input unit to storage"),
                       ("view_storage_perm", "Can see storage"),)

    def __str__(self):
        return self.name
