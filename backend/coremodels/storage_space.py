from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit

class StorageSpace(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    orderpoint = models.PositiveSmallIntegerField(default=0)
    standard_order_amount = models.PositiveSmallIntegerField(default=0)
    maximal_capacity = models.PositiveSmallIntegerField(default=0, null = False)
    amount = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.storageUnit) + " " + str(self.article)