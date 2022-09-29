from backend.services.IstorageManagementService import IstorageManagementService
from backend.coremodels.storage import Storage
from backend.__init__ import si 

@si.register(name = 'storageManagementService')
class storageManagementService(IstorageManagementService):
    def getStorageById(self, id: str) -> Storage:
        try:
            storage = Storage.objects.get(id=id)
            return storage
        except:
            return None