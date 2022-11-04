# from imp import new_module
from django.db import models
from backend.coremodels.article import Article


class AlternativeArticleName(models.Model):
    '''Insert description.'''
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)
