from Web.backend.coremodels.article import Article
from Web.backend.views.views import article
from backend.services.IstorageManagementService import IstorageManagementService
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.transaction import Transaction
from backend.coremodels.inputOutput import InputOutput
from backend.__init__ import si


@si.register(name='storageManagementService')
class storageManagementService(IstorageManagementService):
    def getStorageUnitById(self, id: str) -> StorageUnit:
        try:
            storage = StorageUnit.objects.get(id=id)
            return storage
        except:
            return None

    def getStorageSpaceById(self, id: str) -> StorageSpace:
        try:
            storage = StorageSpace.objects.get(id=id)
            return storage
        except:
            return None

    def setStorage(id: str, amount: int) -> int:
        try:
            newAmount = amount
            return StorageSpace.objects.update(**{amount: newAmount})
        except:
            return None

    def addToStorage(id: str, amount: int) -> int:
        try:
            newAmount = StorageSpace.objects.get(id=id).amount + amount
            return StorageSpace.objects.update(**{amount: newAmount})
        except:
            return None

    def getStock(id: str, article_id: str) -> int:
        try:
            stock = int(StorageSpace.objects.get(
                id=id, article=article_id).amount)
            return stock
        except:
            return None

    def getStorageUnitStock(id: str) -> dict:
        try:
            return "article: {} amount: {}".format(StorageSpace.objects.get(id=id).article, StorageSpace.objects.get(id=id).amount)
        except:
            return None

# FR 10.1.3 #

    def addToStorage2(id: str, amount: int, addOutputUnit: bool) -> Transaction:
        storage_space = StorageSpace.objects.get(id=id)
        storage_unit_id= storage_space.storage_unit
        article = Article.objects.get(id=storage_space.article)
        inputOutput = InputOutput.objects.get(article = article)
        converter= inputOutput.outputUnitPerInputUnit

        if(addOutputUnit):
            newAmount = StorageSpace.objects.get(id=id).amount + amount
        else:
            newAmount = StorageSpace.objects.get(id=id).amount + amount*converter
        
        if (newAmount<0):
            return None
        else:
            StorageSpace.objects.update(**{amount: newAmount})
            try:
                new_transaction = Transaction.objects.create(toStorageUnit=storage_unit_id, article = article, amount=newAmount )
                new_transaction.save()
                return new_transaction
            except:
                return None

    
    def getArticleInStorageSpace(storageSpaceId: str) -> Article:
        try:
            storage_space = StorageSpace.objects.get(id=storageSpaceId)
            article= Article.objects.get(id=storage_space.article)
            return article
        except:
            return None
    
    def searchArticleInStorage(storageUnitId: str, articleId: str) -> int:
        try:
            storage_unit = StorageUnit.objects.get(id=storageUnitId)
            storage_space = StorageSpace.objects.get(storage_unit=storage_unit.id, article=articleId)
            return storage_space.amount
        except:
            return None
# FR 10.1.3 #
