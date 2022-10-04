from unittest.util import _MAX_LENGTH
from django.db import models

class StorageUnit(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=30)
    building = models.CharField(max_length=30)
    floor = models.CharField(max_length= 30)

    def __str__(self):
        return self.name