from django.db import models
from backend.coremodels.article import Article
from backend.coremodels.supplier import Supplier


class ArticleHasSupplier(models.Model):
    '''Article has supplier.'''
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    supplier_article_nr = models.CharField(max_length=15, null=True)
    article_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.article_supplier)
