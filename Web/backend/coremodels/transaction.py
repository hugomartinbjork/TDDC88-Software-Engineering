from django.db import models
from backend.coremodels.storage import Storage
from django.contrib.auth.models import User
from backend.coremodels.article import Article
from backend.operations.enumerator import TransactionOperator
from django.utils.timezone import now
# from datetime import datetime
# Transaction to or from storageUnit by User


class Transaction(models.Model):
    '''Transaction.'''
    id = models.AutoField(primary_key=True, null=False)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)
    time_of_transaction = models.DateField(
        default=now, null=True, blank=True)
    operation = models.IntegerField(
        choices=TransactionOperator.choices, default=0, null=False)


    class Meta:
        permissions = (("get_all_transaction", "Can get all transactions"),
        ("get_transaction_by_id", "Can get a transaction by id"),
        ("get_user_transactions", "Can get a users transactions"),)

    def __str__(self):
        return str(self.id)

    def get_value(self):
        return self.article.price*self.amount
