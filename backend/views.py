from django.shortcuts import render
from rest_framework import generics
from core.models import Storage, storageUnit, Article
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from .serializers import StorageSerializer, StorageUnitSerializer, ArticleSerializer
from django.views import View
from services import IarticleManagementService

# Create your views here.
class storageList(generics.ListCreateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

class article(View):  
    def get(self, request, articleId): 
        try:
            article = Article.objects.get(lioId = articleId)
        except:
            return Http404('Could not find article') 
        serializer = ArticleSerializer(article)
        if serializer.is_valid:
            return JsonResponse(serializer.data, status=200)
        return HttpResponseBadRequest