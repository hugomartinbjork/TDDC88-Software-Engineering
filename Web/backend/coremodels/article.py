# from tkinter import CASCADE
# from unittest.util import _MAX_LENGTH
from django.db import models
from backend.coremodels.group import GroupInfo
from backend.operations.enumerator import UnitOperator
# from backend.coremodels.storageComponent import storageComponent


class Article(models.Model):
    '''Article.'''
    lio_id = models.CharField(max_length=15, primary_key=True)
    description = models.CharField(max_length=100, null=True)
    price = models.IntegerField(null=True)
    name = models.CharField(max_length=30)
    Z41 = models.BooleanField(default=False)  # Change to boolean because Z41
    # is true or false
    image = models.ImageField(null=True, blank=True)
    article_group = models.ManyToManyField(GroupInfo)  # Look at database
    # schema and requirement
    alternative_articles = models.ManyToManyField('self', blank=True)
    # The following four lines might make inputOuput.py obsolete // FH
    refill_unit = models.IntegerField(
        choices=UnitOperator.choices, default=1, null=False)
    takeout_unit = models.IntegerField(
        choices=UnitOperator.choices, default=1, null=False)

    class Meta:
        permissions = (("get_article", "Can get articles from database"),)

    # Should these attributes below really be included, they are not
    # included in the database schema??

#     std_cost = models.IntegerField(null = True)
#     minimal_order_qt = models.IntegerField(null = True)
#     refill_unit = models.IntegerField(null = True)
#     take_out_unit = models.IntegerField(null = True)
#     alternative_names = models.TextField(null=True, blank=True)
#     alternative_articles = models.ManyToManyField('self', blank = True)
#     supplier = models.CharField(max_length=30, null = True)
#     sup_ordernr = models.IntegerField(null = True)
#    # storageComponent = models.CharField(max_length=15, null = True)

    def __str__(self):
        return self.name
