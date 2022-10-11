from http.client import OK
import pkgutil
from urllib import request
import json
from django.shortcuts import render
from rest_framework import generics
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from ..serializers import StorageUnitSerializer, ArticleSerializer, GroupSerializer, QRCodeSerializer, OrderSerializer
# This import is important for now, since the dependency in articlemanagmentservice will not be stored in the serviceInjector otherwise however, I'm
# hoping to be able to change this since it looks kind of trashy
from backend.services.articleManagementService import articleManagementService
from backend.services.userService import userService
from backend.services.groupManagementService import groupManagementService
from backend.services.storageManagementService import storageManagementService
from backend.services.orderServices import OrderService
from django.views import View
from backend.__init__ import si
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.qr_code import QRCode
from backend.coremodels.order import Order
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


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
                raise Http404("Could not find group")
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
            serializer = StorageUnitSerializer(storage)
            if serializer.is_valid:
                return JsonResponse(serializer.data, status=200)
            return HttpResponseBadRequest



class order(View): 
    @si.inject #Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing 
    def __init__(self, _deps):
        OrderService = _deps['OrderService']
        self._orderService = OrderService() #Instance of dependency is created in constructor
    def get(self, request, id): 
        if request.method == 'GET':
            order = self._orderService.getOrderById(id)
            if order is None:
                raise Http404("Could not find order")
            serializer = OrderSerializer(order)
            if serializer.is_valid:
                return JsonResponse(serializer.data, status=200)
            return HttpResponseBadRequest

    
    def post(self, request, id):
        if request.method == 'POST':
            json_body = json.loads(request.body)
            article = json_body['ofArticle']
            storageUnit = json_body['toStorageUnit']
            amount = json_body['amount']
            if(OrderService.has_order(self, storageUnit, article) is not None):
                order = OrderService.has_order(self, storageUnit, article)
                eta = {"Expected arrival: " : OrderService.getETA(self, order.id)}
                return JsonResponse(eta, status=200)
            else:
                order =OrderService.place_order(self, storageUnit, article, amount)
                serializer = OrderSerializer(order)
                if serializer.is_valid:
                    return JsonResponse(serializer.data, status=200)



class Login(APIView):
    @si.inject #Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing 
    def __init__(self, _deps):
        userService = _deps['userService']
        self._userService = userService()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please fill in all fields'}, status=status.HTTP_400_BAD_REQUEST)

        check_user = User.objects.filter(username=username).exists()
        if check_user == False:
            return Response({'error': 'Username does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            return self._userService.createAuthToken(request, user)
        else:
            return Response({'error': 'invalid details'}, status=status.HTTP_400_BAD_REQUEST)


class LoginWithId(APIView):
    @si.inject
    def __init__(self, _deps):
        userService = _deps['userService']
        self._userService = userService()

    def post(self, request):
        user_id = request.data.get('id')

        check_user = User.objects.filter(id=user_id).exists()
        if check_user == False:
            return Response({'error': 'User ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user = self._userService.authenticatewithid(id=user_id)
        if user is not None:
            return self._userService.createAuthToken(request, user)
        else:
            return Response({'error': 'invalid details'}, status=status.HTTP_400_BAD_REQUEST)
