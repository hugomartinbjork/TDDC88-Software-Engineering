from django.db import models
from backend.coremodels.storage_unit import StorageUnit
from django.contrib.auth.models import User
from backend.coremodels.article import Article

#Transaction to or from storageUnit by User
class Transaction(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    operation = models.CharField(max_length=30, null = True)

    def __str__(self):
        return str(self.id)

