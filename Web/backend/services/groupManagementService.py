from backend.coremodels.group import GroupInfo
from backend.__init__ import serviceInjector as si
# from ..__init__ import dataAccessInjector as di


@si.register(name='GroupManagementService')
class GroupManagementService():

    def get_group_by_id(self, id: str) -> GroupInfo:
        try:
            group = GroupInfo.objects.get(id=id)
            return group
        except Exception:
            return None
