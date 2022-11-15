from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.order import Order
from backend.operations.enumerator import OrderedUnitOperator


class OrderedArticle(models.Model):
    '''Order.'''
    id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField(default=None)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit = models.CharField(max_length=10,
                            choices=OrderedUnitOperator.choices, default=OrderedUnitOperator.INPUT)


    def __str__(self):
        return (str(self.id)
                + ": " + str(self.article)
                + " " + str(self.order)
                + " " + str(self.id))
