from datetime import datetime
from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.operations.enumerator import OrderOperator


class Order(models.Model):
    '''Order.'''
    id = models.AutoField(primary_key=True)
    of_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    to_storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=None)
    expected_wait = models.PositiveSmallIntegerField(default=0)
    order_time = models.DateTimeField(default=datetime.now)
    order_state = models.IntegerField(
        choices=OrderOperator.choices, default=1, null=False)


    def __str__(self):
        return (str(self.id)
                + ": " + str(self.of_article)
                + " " + str(self.to_storage))
