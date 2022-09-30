from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from backend.__init__ import si


@si.register()
class userService():

    def getAuthtokenId(self, id):
        token = Token.objects.get(user=id).key
        return token

    def getAuthtoken(self, username, password):
        user = User.objects.get(username=username)
        if user.check_password(password):
            token = Token.objects.get(user=user.id).key
            return token
        else:
            return None
