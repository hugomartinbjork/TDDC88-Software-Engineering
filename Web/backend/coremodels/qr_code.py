# from tkinter import CASCADE
from django.db import models
from backend.coremodels.storage_space import StorageSpace


class QRCode(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    storage_space = models.ForeignKey(StorageSpace, on_delete=models.CASCADE,
                                      null=True)

    def __str__(self):
        return self.id
