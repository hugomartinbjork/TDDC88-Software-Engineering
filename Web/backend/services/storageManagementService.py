#from requests import request
#from Web.backend.views.views import Compartment
from backend.dataAccess.orderAccess import orderAccess
from backend.dataAccess.storageAccess import storageAccess
from backend.dataAccess.userAccess import userAccess
from backend.serializers import OrderSerializer, StorageSpaceSerializer
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.transaction import Transaction
from backend.coremodels.inputOutput import InputOutput
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.utils.dateparse import parse_date
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di
import random


@si.register(name='storageManagementService')
class storageManagementService():
    @di.inject
    def __init__(self, _deps):
        self._storageAccess: storageAccess = _deps["storageAccess"]()
        self._orderAccess: orderAccess = _deps["orderAccess"]()
        self._userAccess: userAccess = _deps["userAccess"]()

    def getStorageUnitById(self, id: str) -> StorageUnit:
        return self._storageAccess.get_storage(id)

    def getStorageSpaceById(self, id: str) -> StorageSpace:
        return self._storageAccess.get_compartment_by_id(id)

    def getStorageSpaceByArticle(self, article: Article) -> StorageSpace:
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
        compartments = self._storageAccess.get_compartments_by_storage(
            storageId=id)
        value = 0
        for compartment in compartments:
            value += compartment.article.price * compartment.amount
        return value

    def getAllTransactions(self) -> dict:
        return self._storageAccess.get_all_transactions()
    # Storage is not connected to a costcenter atm
    # For now this is sum och costs (takeout-return)
    # from transactions for one storage_compartment
    
    def getStorageCost(self, storage_id: str, start_date: str, end_date: str) -> int:
        start_date_date = parse_date(start_date)
        end_date_date = parse_date(end_date)
        transactions = self._storageAccess.get_transaction_by_storage(
            storageId=storage_id)
        print(transactions)
        sum_value = 0
        takeout_value = 0
        return_value = 0
        for transaction in transactions:
            transaction_date = transaction.time_of_transaction
            transaction_date_date = transaction_date  # .date()
            user_cost_center = self._userAccess.get_user_cost_center(
                transaction.by_user)
            if (user_cost_center == transaction.storage_unit.cost_center):
                if (start_date_date <= transaction_date_date and end_date_date >= transaction_date_date):
                    #transaction_user = transaction.by_user
                    #cost_center = self._userAccess.get_user_cost_center(user=transaction_user)
                    # if cost_center == transaction.storage_id.cost_center
                    if transaction.operation == 1:
                        takeout_value = transaction.get_value()
                    if transaction.operation == 2:
                        return_value = transaction.get_value()
        sum_value = takeout_value - return_value
        return sum_value

    def get_storage_by_costcenter(self, cost_center: str) -> StorageUnit:
        return self._storageAccess.get_storage_by_costcenter(cost_center)

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
        if (addOutputUnit):
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
            new_transaction = Transaction.objects.create(storage_unit=storage_unit_id, article=article, operation=3, by_user=user, amount=new_amount)
            new_transaction.save()
            print("New add transaction created:")
            print(new_transaction)
            return new_transaction
            # except:
            # return None

# TODO: This is a lot of work to refactor since barely any of the methods work. Leaving this
# TODO to the original author

    def addToReturnStorage(self, space_id: str, amount: int, username: str, addOutputUnit: bool) -> Transaction:
        storage_space = StorageSpace.objects.get(id=space_id)
        storage_unit_id = storage_space.storage_unit
        amount = amount
        article = Article.objects.get(lioId=storage_space.article.lioId)
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

        if (medical_employee and article.sanitation_level == 'Z41'):
            return None

        if (addOutputUnit):
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
            new_transaction = Transaction.objects.create(storage_unit=storage_unit_id, article=article, operation=2, by_user=user, amount=new_amount)
            new_transaction.save()
            print("New return transaction created:")
            print(new_transaction)
            return new_transaction

    def takeFromCompartment(self, space_id, amount, username, addOutputUnit):
        compartment = self._storageAccess.get_compartment_by_id(id=space_id)
        article = Article.objects.get(lioId=compartment.article.lioId)
        inputOutput = InputOutput.objects.get(article=article)
        converter = inputOutput.outputUnitPerInputUnit
        user = User.objects.get(username=username)
        if(addOutputUnit):
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount - amount
            new_amount = amount
        else:
            # eftersom det inte verkar finnas funktionalitet för input/output-amounts så har jag satt denna till 2 bara för testningens skull.
            if not converter:
                converter = 2
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount - amount*converter
            new_amount = amount*converter
        if (amount_in_storage < 0):
            return None
        else:
            StorageSpace.objects.update(amount=amount_in_storage)
            new_transaction = Transaction.objects.create(storage_unit=compartment.storage_unit, article=article, operation=1, by_user=user, amount=new_amount)
            new_transaction.save()
            print("New add transaction created:")
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

    ##  FR 9.4.1 och FR 9.4.2 ##
    def create_compartment(self, storage_id: str, placement: str, qr_code: str) -> StorageSpace:

        print(storage_id)
        compartment = self._storageAccess.create_compartment(
            storage_id=storage_id, placement=placement, qr_code=qr_code
        )
        return compartment

    def get_compartment_by_qr(self, qr_code: str) -> StorageSpace:
        compartment = self._storageAccess.get_compartment_by_qr(
            qr_code=qr_code)
        return compartment

    ##  FR 9.4.1 och FR 9.4.2 ##
