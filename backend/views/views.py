from django.shortcuts import render
from rest_framework import generics
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from ..serializers import StorageSerializer, ArticleSerializer, GroupSerializer
# This import is important for now, since the dependency in articlemanagmentservice will not be stored in the serviceInjector otherwise however, I'm
# hoping to be able to change this since it looks kind of trashy
from backend.services.articleManagementService import articleManagementService
from backend.services.groupManagementService import groupManagementService
# hoping to be able to change this since it looks kind of trashy
from backend.services.storageManagementService import storageManagementService
from django.views import View
from backend.__init__ import si
from backend.coremodels.article import Article
from backend.coremodels.storageUnit import StorageUnit
from backend.coremodels.storageSpace import StorageSpace

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


class group(View):
    # Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps):
        groupManagementService = _deps['groupManagementService']
        # Instance of dependency is created in constructor
        self._groupManagementService = groupManagementService()

    def get(self, request, groupId):
        if request.method == 'GET':
            group = self._groupManagementService.getGroupById(groupId)
            if group is None:
                raise Http404("Could not find article")
            serializer = GroupSerializer(group)


class storage(View):
    # Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps):
        storageManagementService = _deps['storageManagementService']
        # Instance of dependency is created in constructor
        self._storageManagementService = storageManagementService()

    def get(self, request, storageId):
        if request.method == 'GET':
            storage = self._storageManagementService.getStorageById(storageId)
            if storage is None:
                raise Http404("Could not find storage")
            serializer = StorageSerializer(storage)
            if serializer.is_valid:
                return JsonResponse(serializer.data, status=200)
            return HttpResponseBadRequest
