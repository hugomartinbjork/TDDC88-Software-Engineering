# from tkinter import CASCADE
from django.db import models
from backend.coremodels.compartment import Compartment


class QRCode(models.Model):
    '''QR code for storage spaces (compartments).'''
    id = models.CharField(max_length=15, primary_key=True)
    compartment = models.ForeignKey(Compartment, on_delete=models.CASCADE,
                                      null=True)

    def __str__(self):
        return str(self.id)
