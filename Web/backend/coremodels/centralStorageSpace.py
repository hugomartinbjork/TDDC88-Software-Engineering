# from datetime import datetime
# from tkinter import CASCADE
# from unittest.util import _MAX_LENGTH
# from xmlrpc.client import NOT_WELLFORMED_ERROR
from django.db import models
from backend.coremodels.article import Article


class CentralStorageSpace(models.Model):
    '''Central storage space.'''
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.id) + ": " + str(self.article) + " " + str(self.amount)
