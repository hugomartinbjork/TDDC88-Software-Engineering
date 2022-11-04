from datetime import datetime
from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    of_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    to_storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=None)
    expected_wait = models.PositiveSmallIntegerField(default=0)
    order_time = models.DateTimeField(default=datetime.now)
    has_arrived = models.BooleanField(default=False)

    def __str__(self):
        return (str(self.id)
                + ": " + str(self.of_article)
                + " " + str(self.to_storage_unit))
