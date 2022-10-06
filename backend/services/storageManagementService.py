from backend.services.IstorageManagementService import IstorageManagementService
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.__init__ import si


@si.register(name='storageManagementService')
class storageManagementService(IstorageManagementService):
    def getStorageById(self, id: str) -> StorageUnit:
        try:
            storage = StorageUnit.objects.get(id=id)
            return storage
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
            stock = int(StorageSpace.objects.get(id=id, article=article_id).amount)
            return stock
        except:
            return None

    def getStorageUnitStock(id: str) -> dict:
        try:
            return "article: {} amount: {}".format(StorageSpace.objects.get(id=id).article, StorageSpace.objects.get(id=id).amount)
        except:
            return None
