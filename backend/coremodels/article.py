from django.db import models

class Article(models.Model):
    name = models.CharField(max_length=30)
    lioId = models.CharField(max_length=15, primary_key=True)
    def __str__(self):
        return self.name