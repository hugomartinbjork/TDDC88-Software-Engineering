from django.db import models
from backend.coremodels.storage import Storage
from django.contrib.auth.models import User
from backend.coremodels.article import Article
from backend.coremodels.cost_center import CostCenter
from backend.operations.enumerator import TransactionOperator, OrderedUnitOperator
from django.utils.timezone import now
# from datetime import datetime
# Transaction to or from storageUnit by User


class Transaction(models.Model):
    '''Transaction.'''
    id = models.AutoField(primary_key=True, null=False)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    attribute_cost_to = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)
    time_of_transaction = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    unit = models.CharField(
        max_length=100, choices=OrderedUnitOperator.choices, default="output", null=False)
    operation = models.CharField(
        max_length=100, choices=TransactionOperator.choices, default="return", null=False)

    class Meta:
        permissions = (("get_all_transaction", "Can get all transactions"),
                       ("get_transaction_by_id", "Can get a transaction by id"),
                       ("get_user_transactions", "Can get a users transactions"),
                       ("replenish", "Can replenish articles to compartment"),
                       ("move_article", "Can move articles between compartments"),)

    def __str__(self):
        return str(self.id)

    def get_value(self):
        return self.article.price*self.amount
