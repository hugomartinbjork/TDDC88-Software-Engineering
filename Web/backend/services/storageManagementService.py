from requests import request
from backend.dataAccess.orderAccess import orderAccess
from backend.dataAccess.storageAccess import storageAccess
from backend.serializers import OrderSerializer, StorageSpaceSerializer
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.transaction import Transaction
from backend.coremodels.inputOutput import InputOutput
from django.contrib.auth.models import User
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di
import random


@si.register(name='storageManagementService')
class storageManagementService():
    @di.inject
    def __init__(self, _deps):
        self._storageAccess: storageAccess = _deps["storageAccess"]()
        self._orderAccess: orderAccess = _deps["orderAccess"]()

    def getStorageUnitById(self, id: str) -> StorageUnit:
        return self._storageAccess.get_storage(id)

    def getStorageSpaceById(self, id: str) -> StorageSpace:
        return self._storageAccess.get_compartment_by_id(id)

    def setStorage(self, id: str, amount: int) -> int:
        return self._storageAccess.set_storage_amount(compartmendId=id, amount=amount)

    def getStock(self, id: str, article_id: str) -> int:
        return self._storageAccess.get_compartment_stock(compartmentId=id, article_id=article_id)

    def getStorageUnitStock(self, id: str) -> dict:
        return self._storageAccess.get_storage_stock(storageId=id)

    def getAllStorageUnits(self) -> dict:
        return self._storageAccess.get_all_storage_units()

    def getStorageValue(self, id: str) -> int:
        compartments = self._storageAccess.get_compartments_by_storage(storageId=id)
        value = 0
        for compartment in compartments:
            value += compartment.article.price * compartment.amount
        return value

# FR 10.1.3 #


# alltid takeout/takein
# TODO: This is a lot of work to refactor since barely any of the methods work. Leaving this
# TODO to the original author


    def addToStorage(self, space_id: str, amount: int, username: str, addOutputUnit: bool) -> Transaction:
        storage_space = self._storageAccess.get_compartment_by_id(
            id=space_id)
        storage_unit_id = storage_space.storage_unit
        article = Article.objects.get(lioId=storage_space.article.lioId)
        inputOutput = InputOutput.objects.get(article=article)
        converter = inputOutput.outputUnitPerInputUnit
        user = User.objects.get(username=username)
        if(addOutputUnit):
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount + amount
            new_amount = amount
        else:
            # eftersom det inte verkar finnas funktionalitet för input/output-amounts så har jag satt denna till 2 bara för testningens skull.
            if not converter:
                converter = 2
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount + amount*converter
            new_amount = amount*converter
        if (amount_in_storage < 0):
            return None
        else:
            StorageSpace.objects.update(amount=amount_in_storage)
            # the auto increment function of id in django bängade ur, so I just created my own ids for Transaction. This is crazy ugly.
            random_id = random.randint(1, 9999)
            if Transaction.objects.filter(id=random_id):
                random_id += 1
            new_transaction = Transaction.objects.create(id=random_id,
                                                         storage_unit=storage_unit_id, article=article, operation=3, by_user=user, amount=new_amount)
            new_transaction.save()
            print("New add transaction created:")
            print(new_transaction)
            return new_transaction
            # except:
            # return None

# TODO: This is a lot of work to refactor since barely any of the methods work. Leaving this
# TODO to the original author

    def addToReturnStorage(space_id: str, amount: int, username: str, addOutputUnit: bool) -> Transaction:
        storage_space = StorageSpace.objects.get(id=space_id)
        storage_unit_id = storage_space.storage_unit
        amount = amount
        article = Article.objects.get(lioId=storage_space.article)
        user = User.objects.get(username=username)
        medical_employee = User.objects.get(username=username).groups.filter(
            name='medical employee').exists()
        inputOutputCheck = InputOutput.objects.filter(article=article).exists()
        if (inputOutputCheck):
            print("inne i första if")
            inputOutput = InputOutput.objects.get(article=article)
            converter = inputOutput.outputUnitPerInputUnit
        else:
            print("inne i else")
            inputOutput = InputOutput.objects.create(article=article)
            converter = inputOutput.outputUnitPerInputUnit

        if(medical_employee and article.sanitation_level == 'Z41'):
            return None

        if(addOutputUnit):
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount + amount
            new_amount = amount
        else:
            if not converter:
                converter = 2
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount + amount*converter
            new_amount = amount*converter
        if (amount_in_storage < 0):
            return None
        else:
            StorageSpace.objects.update(amount=amount_in_storage)
            # the auto increment function of id in django bängade ur, so I just created my own ids for Transaction. This is crazy ugly.
            random_id = random.randint(1, 9999)
            if Transaction.objects.filter(id=random_id):
                random_id += 1
            new_transaction = Transaction.objects.create(id=random_id,
                                                         storage_unit=storage_unit_id, article=article, operation=2, by_user=user, amount=new_amount)
            new_transaction.save()
            print("New return transaction created:")
            print(new_transaction)
            return new_transaction

    def getArticleInStorageSpace(self, storageSpaceId: str) -> Article:
        return self._storageAccess.getArticleInStorageSpace(storageSpaceId=storageSpaceId)

    def searchArticleInStorage(self, storageUnitId: str, articleId: str) -> int:
        return self._storageAccess.searchArticleInStorage(storageUnitId=storageUnitId, articleId=articleId)
# FR 10.1.3 #

    def getCompartmentContentAndOrders(self, compartmentId):
        compartment = self._storageAccess.get_compartment_by_id(
            id=compartmentId)
        alteredDict = {}

        if compartment is None:
            return None

        compartmentSerializer = StorageSpaceSerializer(compartment)
        if not compartmentSerializer.is_valid:
            return None
        alteredDict.update(compartmentSerializer.data)

        order = self._orderAccess.get_order_by_article_and_storage(
            compartment.storage_unit.id, compartment.article.lioId)
        if order is not None:
            orderSerializer = OrderSerializer(order)
            eta = self._orderAccess.get_eta(order.id)
            orderDictionary = {"ETA": eta}
            if orderSerializer.is_valid:
                orderDictionary.update(orderSerializer.data)
            alteredDict['Order'] = orderDictionary
            return alteredDict
