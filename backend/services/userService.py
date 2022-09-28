from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


def createToken(user_id):
    token = Token.objects.get_or_create(user = user_id)
    print(token.key)
    return token.key

