# from contextlib import nullcontext
from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage


class Compartment(models.Model):
    '''A single compartment.'''
    id = models.CharField(max_length=15, primary_key=True)  # this is qr_code
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True,
                                blank=True, db_constraint=False)
    order_point = models.PositiveSmallIntegerField(default=0)
    standard_order_amount = models.PositiveSmallIntegerField(default=0)
    maximal_capacity = models.PositiveSmallIntegerField(default=0, null=False)
    amount = models.PositiveSmallIntegerField(default=0)
    placement = models.CharField(max_length=30, null=True)

    class Meta:
        permissions = (("view_compartment_perm", "Can view all compartments"),)
        unique_together = ['storage', 'article']

    def __str__(self):
        return str(self.storage) + " " + str(self.article)
