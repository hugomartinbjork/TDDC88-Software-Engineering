from datetime import datetime
from django.db import models
from backend.coremodels.article import Article
from django.contrib.auth.models import User
from backend.coremodels.storage_unit import StorageUnit


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    toStorageUnit = models.ForeignKey(StorageUnit.id, on_delete=models.CASCADE)
    byUser = models.ForeignKey(User.username, on_delete=models.CASCADE)
    article = models.ForeignKey(Article.lioId, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=None)
    timeOfTransaction = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.id) + ": " + str(self.byUser) + " " + str(self.toStorageUnit)
