from backend.services.IarticleManagementService import IarticleManagementService
from backend.coremodels.group import GroupInfo
from backend.__init__ import si 

@si.register(name = 'groupManagementService')
class groupManagementService():
    def getGroupById(self, id: str) -> GroupInfo:
        try:
            group = GroupInfo.objects.get(id=id)  
            return group
        except:
            return None