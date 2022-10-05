from datetime import datetime
from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storageUnit import StorageUnit


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    ofArticle = models.ForeignKey(Article, on_delete=models.CASCADE)
    toStorageUnit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=None)
    expectedWait = models.PositiveSmallIntegerField(default=0)
    orderTime = models.DateTimeField(default=datetime.now)
    hasArrived = models.BooleanField(default=False)

    def __str__(self):
        return self.id + ": " + self.ofArticle + " " + self.toStorageUnit
