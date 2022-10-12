from datetime import datetime
from unittest.util import _MAX_LENGTH
from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit


class InputOutput(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    inputUnitName=models.CharField(max_length=30)
    outputUnitName = models.CharField(max_length=30)
    outputUnitPerInputUnit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id) + ": " + str(self.article) + " " + str(self.outputUnitPerInputUnit)
