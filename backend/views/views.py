from django.shortcuts import render
from rest_framework import generics
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from ..serializers import StorageSerializer, ArticleSerializer
#This import is important for now, since the dependency in articlemanagmentservice will not be stored in the serviceInjector otherwise however, I'm
from backend.services.articleManagementService import articleManagementService #hoping to be able to change this since it looks kind of trashy
from django.views import View
from backend.__init__ import si
from backend.coremodels.article import Article 
from backend.coremodels.storage import Storage
from backend.coremodels.storageComponent import storageUnit
from ..services.userService import createToken


# Create your views here.

class article(View): 
    @si.inject #Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing 
    def __init__(self, _deps):
        articleManagementService = _deps['articleManagementService']
        self._articleManagementService = articleManagementService() #Instance of dependency is created in constructor
    def get(self, request, articleId): 
        if request.method == 'GET':
            article = self._articleManagementService.getArticleByLioId(articleId)
            if article is None:
                raise Http404("Could not find article")
            serializer = ArticleSerializer(article)
            if serializer.is_valid:
                return JsonResponse(serializer.data, status=200)
            return HttpResponseBadRequest


def login_user(request):
    id= request['id']
    token=createToken(id)
    return JsonResponse(token)

    