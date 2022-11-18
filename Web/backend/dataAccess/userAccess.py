from backend.coremodels.user_info import UserInfo
from backend.coremodels.cost_center import CostCenter
from django.contrib.auth.models import User
from ..__init__ import dataAccessInjector as di
from rest_framework.authtoken.models import Token


@di.register(name="UserAccess")
class UserAccess():
    '''User access.'''

    def get_user_with_barcode(barcode_id) -> User:
        '''Returns user corresponding to the sent in barcode id, 
        or None if user does not exist.'''
        try:
            return UserInfo.objects.filter(barcode_id=barcode_id).first()
        except Exception:
            return None

    def get_user_with_nfc(nfc_id) -> User:
        '''Returns user corresponding to the sent in nfc id, 
        or None if user does not exist.'''
        try:
            return UserInfo.objects.filter(nfc_id=nfc_id).first()
        except Exception:
            return None

    def get_user_cost_center(self, user: User) -> CostCenter:
        '''Return cost center of user.'''
        try:
            user_info = UserInfo.objects.get(user=user)
            cost_center = user_info.cost_center
            return cost_center
        except Exception:
            return None

    def create_auth_token(request):
        '''Creates and returns authentication token for user in request.'''
        try:
            token, created = Token.objects.get_or_create(user=request.user)
            return token.key
        except Exception:
            return None

    def get_user_info(user_id):
        try:
            return UserInfo.objects.filter(user=user_id).first()
        except Exception:
            return None
