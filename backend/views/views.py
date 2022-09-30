from tokenize import Token
from django.shortcuts import render
from rest_framework import generics
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from ..serializers import StorageSerializer, ArticleSerializer
# This import is important for now, since the dependency in articlemanagmentservice will not be stored in the serviceInjector otherwise however, I'm
# hoping to be able to change this since it looks kind of trashy
from backend.services.articleManagementService import articleManagementService
from backend.services.userService import userService
from django.views import View
from backend.__init__ import si
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.coremodels.storageComponent import storageUnit
#from ..services.userService import createToken


# Create your views here.

class article(View):
    # Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps):
        articleManagementService = _deps['articleManagementService']
        # Instance of dependency is created in constructor
        self._articleManagementService = articleManagementService()

    def get(self, request, articleId):
        if request.method == 'GET':
            article = self._articleManagementService.getArticleByLioId(
                articleId)
            if article is None:
                raise Http404("Could not find article")
            serializer = ArticleSerializer(article)
            if serializer.is_valid:
                return JsonResponse(serializer.data, status=200)
            return HttpResponseBadRequest


class login_user_with_id(View):
    @si.inject
    def __init__(self, _deps):
        userService = _deps['userService']
        self._userService = userService()

    def get(self, request, userId):
        if request.method == 'GET':
            token = self._userService.getAuthtokenId(userId)
        if token is None:
            raise Http404('Could not find user')
        return JsonResponse({'token': token}, status=200)


class login_user(View):
    @si.inject
    def __init__(self, _deps):
        userService = _deps['userService']
        self._userService = userService()

    def get(self, request, username, password):
        if request.method == 'GET':
            token = self._userService.getAuthtoken(username, password)
        if token is None:
            raise Http404('Could not find user')
        return JsonResponse({'token': token}, status=200)
