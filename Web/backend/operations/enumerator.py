from django.db import models


class TransactionOperator(models.IntegerChoices):
    '''Transation operator.'''
    TAKEOUT = 1
    RETURN = 2
    REPLENISH = 3
    ADJUST = 4

class OrderOperator(models.IntegerChoices):
    """Order operator that keeps track of our curretn state"""
ORDER_PLACED = 1
HANDLED_AT_THE_CENTRAL_DEPOT = 2
IN_TRANSIT = 3
DELIVERED = 4
IN_STORAGE = 5



class UnitOperator(models.IntegerChoices):
    '''Unit operator.'''
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
