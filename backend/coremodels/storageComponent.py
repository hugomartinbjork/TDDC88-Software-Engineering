from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage

class storageUnit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    currentStock = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return str(self.storage) + " " + str(self.article)