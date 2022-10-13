from django.db import models
class TransactionOperator(models.IntegerChoices):
        TAKEOUT = 1
        RETURN = 2
        REPLENISH = 3
        ADJUST = 4
