from backend.coremodels.group import GroupInfo
from backend.__init__ import serviceInjector as si
# from ..__init__ import dataAccessInjector as di


@si.register(name='groupManagementService')
class groupManagementService():

    def getGroupById(self, id: str) -> GroupInfo:
        try:
            group = GroupInfo.objects.get(id=id)
            return group
        except Exception:
            return None
