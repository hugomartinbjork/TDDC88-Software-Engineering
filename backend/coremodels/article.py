from django.db import models

class Article(models.Model):
    name = models.CharField(max_length=30)
    lioId = models.CharField(max_length=15, primary_key=True)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=100, null = True)
    price = models.IntegerField(null = True)
    refill_unit = models.IntegerField(null = True)
    take_out_unit = models.IntegerField(null = True)
    alternative_names = models.TextField(null=True, blank=True)
    alternative_articles = models.ForeignKey('self', on_delete=models.CASCADE, blank = True, null=True)
    supplier = models.CharField(max_length=30, null = True)
    sup_ordernr = models.IntegerField(null = True)
    def __str__(self):
        return self.name