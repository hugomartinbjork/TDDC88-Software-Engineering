from django.db import models

class Supplier(models.Model):
    '''Supplier.'''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)
    supplier_number = models.CharField(max_length=15)

    def __str__(self):
        return str(self.name)
