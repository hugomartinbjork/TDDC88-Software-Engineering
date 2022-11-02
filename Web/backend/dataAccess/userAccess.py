from backend.coremodels.user_info import UserInfo
from backend.coremodels.cost_center import CostCenter
from django.contrib.auth.models import User
from ..__init__ import dataAccessInjector as di



@di.register(name="userAccess")
class userAccess():
    def get_user_cost_center(self, user: User) -> CostCenter:
        try:
            user_info = UserInfo.objects.get(user=user)
            cost_center = user_info.cost_center
            return cost_center
        except:
            return None