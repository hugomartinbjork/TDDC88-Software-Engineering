from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.order import Order


class OrderHasArticle(models.Model):
    '''Order.'''
    id = models.AutoField(primary_key=True)
    quantity = models.PositiveIntegerField(default=None)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.id)
                + ": " + str(self.article)
                + " " + str(self.order)
                + " " + str(self.id))
