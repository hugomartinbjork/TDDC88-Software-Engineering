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
    # Change to boolean because Z41 is true or false
    Z41 = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    article_group = models.ManyToManyField(GroupInfo)  # Look at database
    # schema and requirement
    alternative_articles = models.ManyToManyField('self', blank=True)
    input = models.CharField(max_length=100,
                             choices=UnitOperator.choices, default=UnitOperator.MILLILITRES)
    output = models.CharField(max_length=100,
                              choices=UnitOperator.choices, default=UnitOperator.MILLILITRES)

    output_per_input = models.IntegerField(null=True, default=1)


    class Meta:
        permissions = (
        ("post_article", "Can create an article"),
        ("put_article", "Can edit an article"),
        ("delete_article_new", "Can delete an article"),)


    def __str__(self):
        return self.name
