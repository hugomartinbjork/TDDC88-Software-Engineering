# from genericpath import exists
# from django.conf import settings
from backend.coremodels.transaction import Transaction

from django.contrib.auth.models import User
from backend.__init__ import serviceInjector as si
# from ..__init__ import dataAccessInjector as di
from django.contrib.auth.backends import BaseBackend
from backend.coremodels.user_info import UserInfo
from backend.dataAccess.userAccess import UserAccess


@si.register()
class UserService(BaseBackend):
    '''User service.'''

    def authenticate_with_id(self, id):
        '''Authenticate using id.'''
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def create_auth_token(self, request):
        return UserAccess.create_auth_token(request=request)


    def get_all_transactions_by_user(self, current_user) -> dict:
        '''Return every transaction made by user.'''
        user_convert = list(current_user)
        all_transactions = Transaction.objects.filter(
            by_user=user_convert[0]).all().values()

        return all_transactions

    def get_user_info(self, user_id):
        return UserAccess.get_user_info(user_id)
