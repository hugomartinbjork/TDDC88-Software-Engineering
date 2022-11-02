from django.db import models
from datetime import datetime
#from sqlalchemy import PrimaryKeyConstraint
from backend.coremodels.storage_unit import StorageUnit
from django.contrib.auth.models import User
from backend.coremodels.article import Article
from backend.operations.enumerator import TransactionOperator

#Transaction to or from storageUnit by User
class Transaction(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)
    time_of_transaction = models.DateField(auto_now_add=True, null=False)
    operation = models.IntegerField(
        choices=TransactionOperator.choices, default=0, null=False)

    
    def __str__(self):
        return str(self.id)

    def get_value(self):
        return self.article.price*self.amount


