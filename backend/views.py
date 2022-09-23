from django.shortcuts import render
from rest_framework import generics
from backend.services.articleManagementService import articleManagementService
from backend.models import Storage, storageUnit, Article
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from .serializers import StorageSerializer, StorageUnitSerializer, ArticleSerializer
from django.views import View
from backend.services import IarticleManagementService
from backend.__init__ import si

# Create your views here.
class storageList(generics.ListCreateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

class article(View): 
    @si.inject
    def __init__(self, _deps):
        self._articleManagementService = _deps['articleManagementService']
    def get(self, request, articleId): 
        article = self._articleManagementService.getArticleByLioId(articleId)
        if article is None:
            return Http404("Could not find article")
        
        serializer = ArticleSerializer(article)
        
        if serializer.is_valid:
            return JsonResponse(serializer.data, status=200)
        return HttpResponseBadRequest