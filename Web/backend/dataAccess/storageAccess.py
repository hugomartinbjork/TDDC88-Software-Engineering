from datetime import timedelta
from backend.coremodels.article import Article
from backend.coremodels.transaction import Transaction
#from backend.coremodels.Compartment import Compartment
#from backend.coremodels.Storage import Storage
from backend.coremodels.qr_code import QRCode
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.transaction import Transaction
from ..coremodels.order import Order
from ..__init__ import dataAccessInjector as di

@di.register(name="storageAccess")
class storageAccess():
    def get_storage(self, id: str) -> StorageUnit:
        try:
            storage = StorageUnit.objects.get(id=id)
            return storage
        except:
            return None

    def get_compartment_by_id(self, id: str) -> StorageSpace:
        try:
            storage = StorageSpace.objects.get(id=id)
            return storage
        except:
            return None

    #TODO: This does not seem to do what it is supposed to do. Please review
    def set_storage_amount(self, compartmentId: str, amount: int) -> int:
        try:
            newAmount = amount
            return StorageSpace.objects.update(**{amount: newAmount})
        except:
            return None

    #TODO: This does not seem to do what it is supposed to do. Please review
    def get_compartment_stock(self, compartmentId: str, article_id: str) -> int:
        try:
            stock = int(StorageSpace.objects.get(
                id=id, article=article_id).amount)
            return stock
        except:
            return None

    def get_storage_stock(self, storageId: str) -> dict:
        try:
            return "article: {} amount: {}".format(StorageSpace.objects.get(id=id).article, StorageSpace.objects.get(id=id).amount)
        except:
            return None
    
    def get_all_storage_units(self) -> dict:
        try:
            allStorageUnits = StorageUnit.objects.all().values()  
            return allStorageUnits
        except:
            return None

    def getArticleInStorageSpace(self, storageSpaceId: str) -> Article:
        try:
            storage_space = StorageSpace.objects.get(id=storageSpaceId)
            article= Article.objects.get(id=storage_space.article)
            return article
        except:
            return None
    
    def searchArticleInStorage(self, storageUnitId: str, articleId: str) -> int:
        try:
            storage_unit = StorageUnit.objects.get(id=storageUnitId)
            article = Article.objects.get(lioId = articleId)
            storage_space = StorageSpace.objects.get(storage_unit=storage_unit, article=article)
            return storage_space.amount
        except:
            return None

    def get_compartments_by_storage(self, storageId: str) -> int:
        try: 
            return StorageSpace.objects.filter(storage_unit=storageId)
        except:
            return None
    

    def get_all_transactions(self) -> dict:
        try:
            allTransactions = Transaction.objects.all().values()
            return allTransactions
        except:
            return None
    def get_transaction_by_storage(self, storageId: str) -> int:
        try:
            return Transaction.objects.filter(storage_unit=storageId)
        except:
            return None

    def get_storage_by_costcenter(self, cost_center: str) -> StorageUnit:
        try:
            storage = StorageUnit.objects.get(cost_center=cost_center)
            return storage
        except:
            None

##  FR 9.4.1 och FR 9.4.2 ##

    def create_compartment(self, storage_id: str, placement: str, qr_code) -> StorageSpace:
        print("helelo: " +storage_id)
        storage = StorageUnit.objects.filter(id = storage_id).first()
        article = Article.objects.get(lioId = '123')
        print(storage)
        try:
            compartment = StorageSpace(
            id = qr_code,
            storage_unit = storage, 
            placement = placement,
        )
            compartment.save()
            return compartment
        except:
            return None

    
    def get_compartment_by_qr(self, qr_code: str) -> StorageSpace:
        try:
            compartment = StorageSpace.objects.get(id=qr_code)
            return compartment
        except:
            return None
        

##  FR 9.4.1 och FR 9.4.2 ##
