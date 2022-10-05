from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.Order_text_files.utils import *

class storageComponent(models.Model):
    qrId = models.CharField(max_length=15, primary_key=True, default='0')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)
    standardOrderAmount = models.PositiveSmallIntegerField(default=0)
    orderpoint = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.storage) + " " + str(self.article)

    def getAmount(id):
        amount = storageComponent.objects.get(id=id).amount
        return amount

    def getOrderPoint(id):
        orderpoint = storageComponent.objects.get(id=id).orderpoint
        return orderpoint



  

