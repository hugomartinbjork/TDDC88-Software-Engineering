from backend.services.IarticleManagementService import IarticleManagementService
from backend.coremodels.group import Group
from backend.__init__ import si 

@si.register(name = 'groupManagementService')
class groupManagementService():
    def getGroupById(self, id: str) -> Group:
        try:
            group = Group.objects.get(id=id)  
            return group
        except:
            return None