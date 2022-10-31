from genericpath import exists
from django.contrib.auth import login
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di
from django.contrib.auth.backends import BaseBackend
from rest_framework.response import Response
from rest_framework import status


@si.register()
class userService(BaseBackend):
    def authenticatewithid(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def createAuthToken(self, request, user):
        login(request, user)
        token, created = Token.objects.get_or_create(user=request.user)
        data = {
            'token': token.key,
        }
        return Response({'success': 'successfull login', 'data': data}, status=status.HTTP_200_OK)
        
    def get_all_transactions_by_user(self, id) -> dict:
        return self._storageAccess.get_all_transactions()
