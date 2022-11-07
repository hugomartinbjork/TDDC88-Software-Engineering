from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.utils.dateparse import parse_date
# from sqlalchemy import PrimaryKeyConstraint
from backend.coremodels.storage import Storage
from django.contrib.auth.models import User
from backend.coremodels.article import Article
from backend.operations.enumerator import TransactionOperator
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
        default=now(), null=True, blank=True)
    operation = models.IntegerField(
        choices=TransactionOperator.choices, default=0, null=False)

    def __str__(self):
        return str(self.id)

    def get_value(self):
        return self.article.price*self.amount
