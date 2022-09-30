from genericpath import exists
from django.contrib.auth import login
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from backend.__init__ import si
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


#     def getAuthtokenId(self, id):
#         token = Token.objects.create(user=id).key
#         return token

#     def getAuthtoken(self, username, password):
#         user = User.objects.get(username=username)
#         if user.check_password(password):
#             token = Token.objects.create(user=user.id).key
#             return token
#         else:
#             return None
