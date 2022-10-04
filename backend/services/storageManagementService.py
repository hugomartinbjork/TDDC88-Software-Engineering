from backend.services.IstorageManagementService import IstorageManagementService
from backend.coremodels.storage_unit import StorageUnit
from backend.__init__ import si 

@si.register(name = 'storageManagementService')
class storageManagementService(IstorageManagementService):
    def getStorageById(self, id: str) -> StorageUnit:
        try:
            storage = StorageUnit.objects.get(id=id)
            return storage
        except:
            return None