from backend.services.IstorageManagementService import IstorageManagementService
from backend.coremodels.storage_unit import StorageUnit
<<<<<<< HEAD
from backend.__init__ import si 
=======
from backend.__init__ import si
>>>>>>> 302e67655bc84241798ea3dbbe9f8751aa353bb0


@si.register(name='storageManagementService')
class storageManagementService(IstorageManagementService):
    def getStorageById(self, id: str) -> StorageUnit:
        try:
            storage = StorageUnit.objects.get(id=id)
            return storage
        except:
            return None
