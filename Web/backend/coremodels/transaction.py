from django.db import models
from datetime import datetime
<<<<<<< HEAD
=======

#from sqlalchemy import PrimaryKeyConstraint
>>>>>>> c4910a99f3856d4d9bd71b9487eb63b772fe2c49
from backend.coremodels.storage_unit import StorageUnit
from django.contrib.auth.models import User
from backend.coremodels.article import Article
from backend.operations.enumerator import TransactionOperator

#Transaction to or from storageUnit by User
class Transaction(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    storage_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=0)
<<<<<<< HEAD
    time_of_transaction = models.DateTimeField(auto_now_add=True, null = False)
    operation = models.IntegerField(choices=TransactionOperator.choices,default=0, null = False)
=======
    time_of_transaction = models.DateField(auto_now_add=True, null=False)
    operation = models.IntegerField(
        choices=TransactionOperator.choices, default=0, null=False)
>>>>>>> c4910a99f3856d4d9bd71b9487eb63b772fe2c49

    
    def __str__(self):
<<<<<<< HEAD
        return str(self.id)
=======
        return str(self.id)

    def get_value(self):
        return self.article.price*self.amount


>>>>>>> c4910a99f3856d4d9bd71b9487eb63b772fe2c49
