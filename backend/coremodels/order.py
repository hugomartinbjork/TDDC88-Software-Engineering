from datetime import datetime
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from xmlrpc.client import NOT_WELLFORMED_ERROR
from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    ofArticle = models.ForeignKey(Article, on_delete=models.CASCADE)
    toStorageUnit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    expectedWait = models.PositiveSmallIntegerField(default=0)
    orderTime = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return str(self.id) +": " + str(self.ofArticle) + " " + str(self.toStorageUnit)