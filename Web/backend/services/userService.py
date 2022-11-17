# from genericpath import exists
# from django.conf import settings
from backend.coremodels.transaction import Transaction
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from backend.__init__ import serviceInjector as si
# from ..__init__ import dataAccessInjector as di
from django.contrib.auth.backends import BaseBackend
from rest_framework.response import Response
from rest_framework import status
from backend.coremodels.user_info import UserInfo


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
        '''Create authentication token.'''
        #try:
        token, created = Token.objects.get_or_create(user=request.user)
        print(token.key)
        return token.key
       # except Exception:
       #     return None

    def get_all_transactions_by_user(self, current_user) -> dict:
        '''Return every transaction made by user.'''
        user_convert = list(current_user)
        all_transactions = Transaction.objects.filter(
            by_user=user_convert[0]).all().values()

        return all_transactions

    def get_user_info(self, user_id):
        '''Return user information.'''
        try:
            user_info = UserInfo.objects.get(user=user_id)
            return user_info
        except Exception:
            return None
