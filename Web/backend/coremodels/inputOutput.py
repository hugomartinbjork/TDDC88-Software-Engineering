from datetime import datetime
from unittest.util import _MAX_LENGTH
from django.db import models
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.article import Article


class InputOutput(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    inputUnitName = models.CharField(max_length=30, default="input")
    outputUnitName = models.CharField(max_length=30, default=("output"))
    outputUnitPerInputUnit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id) + ": " + str(self.article) + " " + str(self.outputUnitPerInputUnit)
