# from datetime import datetime
# from unittest.util import _MAX_LENGTH
from django.db import models
from backend.coremodels.article import Article
# from backend.coremodels.storage import Storage


class InputOutput(models.Model):
    '''Describes output/input parameters for articles.'''
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    input_unit_name = models.CharField(max_length=30)
    output_unit_name = models.CharField(max_length=30)
    output_unit_per_input_unit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (str(self.id)
                + ": " + str(self.article)
                + " " + str(self.output_unit_per_input_unit))
