from django.db import models


class TransactionOperator(models.IntegerChoices):
    TAKEOUT = 1
    RETURN = 2
    REPLENISH = 3
    ADJUST = 4


class UnitOperator(models.IntegerChoices):
    MILLILITRES = 1
    CENTILITRES = 2
    DECILITRES = 3
    LITRES = 4
    MILLIMETRES = 5
    CENTIMETRES = 6
    METRES = 7
    PIECES = 8
    CRATES = 9
    BOTTLES = 10
