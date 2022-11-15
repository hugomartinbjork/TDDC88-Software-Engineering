from datetime import datetime
from django.db import models
from backend.coremodels.storage import Storage
from backend.operations.enumerator import OrderOperator


class Order(models.Model):
    '''Order.'''
    id = models.AutoField(primary_key=True)
    to_storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    estimated_delivery_date = models.DateTimeField(null=False)
    order_date = models.DateTimeField(default=datetime.now)
    order_state = models.IntegerField(
        choices=OrderOperator.choices, default=1, null=False)

    class Meta:
        permissions = (("get_order", "Can get orders from database"),)
        
        
        

    def __str__(self):
        return (str(self.id)
                + " " + str(self.to_storage))
