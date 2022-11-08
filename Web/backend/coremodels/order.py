from datetime import datetime
from datetime import timedelta
from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.operations.enumerator import OrderOperator


class Order(models.Model):
    '''Order.'''
    id = models.AutoField(primary_key=True)
    to_storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    estimated_delivery_date = models.DateTimeField(
        default=datetime.now+timedelta(day=14))
    order_date = models.DateTimeField(default=datetime.now)
    order_state = models.IntegerField(
        choices=OrderOperator.choices, default=1, null=False)


    def __str__(self):
        return (str(self.id)
                + " " + str(self.to_storage))
