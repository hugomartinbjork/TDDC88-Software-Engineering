from backend.dataAccess.orderAccess import orderAccess
from backend.dataAccess.storageAccess import storageAccess
from backend.serializers import OrderSerializer, StorageSpaceSerializer
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.transaction import Transaction
from backend.coremodels.inputOutput import InputOutput
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di


@si.register(name='storageManagementService')
class storageManagementService():
    @di.inject
    def __init__(self, _deps):
        self._storageAccess : storageAccess = _deps["storageAccess"]()
        self._orderAccess : orderAccess = _deps["orderAccess"]()

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

    def getStorageCost(self, id: str) -> int:
        compartments = self._storageAccess.get_compartments_by_storage(storageId=id)
        cost = 0
        for compartment in compartments:
            cost += compartment.article.price * compartment.amount
        return cost

# FR 10.1.3 #


##alltid takeout/takein
# TODO: This is a lot of work to refactor since barely any of the methods work. Leaving this 
# TODO to the original author
    def addToStorage(self, id: str, amount: int,user, addOutputUnit: bool) -> Transaction:
        storage_space = self._storageAccess.get_compartment_by_id(id=id)
        storage_unit_id= storage_space.storage_unit
        article = Article.objects.get(id=storage_space.article)
        inputOutput = InputOutput.objects.get(article = article)
        converter= inputOutput.outputUnitPerInputUnit

        if(addOutputUnit):
            amount_in_storage = StorageSpace.objects.get(id=id).amount + amount
            new_amount=amount
        else:
            amount_in_storage = StorageSpace.objects.get(id=id).amount + amount*converter
            new_amount=amount*converter
        
        if (amount_in_storage<0):
            return None
        else:
            StorageSpace.objects.update(**{amount: amount_in_storage})
            try:
                new_transaction = Transaction.objects.create(storage_unit=storage_unit_id, article = article, operation=1, by_user=user , amount=new_amount )
                new_transaction.save()
                return new_transaction
            except:
                return None

# TODO: This is a lot of work to refactor since barely any of the methods work. Leaving this 
# TODO to the original author

    def addToReturnStorage(id: str, amount: int, user, addOutputUnit: bool) -> Transaction:
        storage_space = StorageSpace.objects.get(id=id)
        storage_unit_id= storage_space.storage_unit
        amount=amount
        article = Article.objects.get(id=storage_space.article)
        inputOutput = InputOutput.objects.get(article = article)
        converter= inputOutput.outputUnitPerInputUnit
        medical_employee = user.groups.filter(name='medical employee').exists()
        if(medical_employee and article.sanitation_level=='Z41'):
            return None

        if(addOutputUnit):
            amount_in_storage = StorageSpace.objects.get(id=id).amount + amount
            new_amount=amount
        else:
            amount_in_storage = StorageSpace.objects.get(id=id).amount + amount*converter
            new_amount=amount*converter
        if (amount_in_storage<0):
            return None
        else:
            StorageSpace.objects.update(**{amount: amount_in_storage})
            try:
                new_transaction = Transaction.objects.create(storage_unit=storage_unit_id, article = article, operation=2, by_user=user, amount=new_amount )
                new_transaction.save()
                return new_transaction
            except:
                return None
    
    def getArticleInStorageSpace(self, storageSpaceId: str) -> Article:
        return self._storageAccess.getArticleInStorageSpace(storageSpaceId=storageSpaceId)
    
    def searchArticleInStorage(self, storageUnitId: str, articleId: str) -> int:
        return self._storageAccess.searchArticleInStorage(storageUnitId=storageUnitId, articleId=articleId)
# FR 10.1.3 #


    def getCompartmentContentAndOrders(self, compartmentId):
        compartment = self._storageAccess.get_compartment_by_id(id=compartmentId)
        alteredDict = {}

        if compartment is None:
            return None

        compartmentSerializer = StorageSpaceSerializer(compartment)
        if not compartmentSerializer.is_valid:
            return None
        alteredDict.update(compartmentSerializer.data)

        order = self._orderAccess.get_order_by_article_and_storage(compartment.storage_unit.id, compartment.article.lioId)
        if order is not None:
            orderSerializer = OrderSerializer(order)
            eta = self._orderAccess.get_eta(order.id)
            orderDictionary = {"ETA": eta}
            if orderSerializer.is_valid:
                orderDictionary.update(orderSerializer.data)
            alteredDict['Order'] = orderDictionary
            return alteredDict
