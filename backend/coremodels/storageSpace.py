from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storageUnit import StorageUnit


class StorageSpace(models.Model):
    qrId = models.CharField(max_length=15, primary_key=True, default='0')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    storage = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)
    standardOrderAmount = models.PositiveSmallIntegerField(default=0)
    orderpoint = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.storage) + " " + str(self.article)
