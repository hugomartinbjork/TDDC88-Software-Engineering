from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models
from backend.coremodels.group import Group
#from backend.coremodels.storageComponent import storageComponent



class Article(models.Model):
    name = models.CharField(max_length=30)
    lioId = models.CharField(max_length=15, primary_key=True)
    article_group = models.ManyToManyField('Group')
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=100, null = True)
    std_cost = models.IntegerField(null = True)
    minimal_order_qt = models.IntegerField(null = True)
    price = models.IntegerField(null = True)
    refill_unit = models.IntegerField(null = True)
    take_out_unit = models.IntegerField(null = True)
    alternative_names = models.TextField(null=True, blank=True)
    alternative_articles = models.ManyToManyField('self', blank = True)
    supplier = models.CharField(max_length=30, null = True)
    sup_ordernr = models.IntegerField(null = True)
   # storageComponent = models.CharField(max_length=15, null = True)

    def __str__(self):
        return self.name










