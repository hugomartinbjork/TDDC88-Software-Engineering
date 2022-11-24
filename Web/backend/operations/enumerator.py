from django.db import models
from django.utils.translation import gettext_lazy as _


class TransactionOperator(models.TextChoices):
    '''Transation operator.'''
    TAKEOUT = "takeout",
    RETURN = "return",
    REPLENISH = "replenish",
    ADJUST = "adjust",


class OrderOperator(models.TextChoices):
    '''Order operator that keeps track of our current state'''
    ORDER_PLACED = "order placed",
    DELIVERED = "delivered",


class UnitOperator(models.TextChoices):
    '''Unit of different input and output units'''
    MILLILITRES = "ml",
    CENTILITRES = "cl",
    DECILITRES = "dl",
    LITRES = "l",
    MILLIMETRES = "mm",
    CENTIMETRES = "cm",
    METRES = "m",
    PIECES = "pieces",
    CRATES = "crates",
    BOTTLES = "bottles"


class OrderedUnitOperator(models.TextChoices):
    '''Unit operator.'''
    INPUT = "input"
    OUTPUT = "output"
