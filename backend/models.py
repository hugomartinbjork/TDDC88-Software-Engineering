from django.db import models

# Create your models here.

class Article(models.Model):
    name = models.CharField(max_length=30)
    lioId = models.CharField(max_length=15, primary_key=True)
    def __str__(self):
        return self.name

class Storage(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class storageUnit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    currentStock = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return str(self.storage) + " " + str(self.article)

