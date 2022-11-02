from http.client import OK
import pkgutil
from urllib import request
import json
from django.shortcuts import render
from backend.dataAccess.storageAccess import storageAccess
from rest_framework import generics
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseBadRequest
from ..serializers import StorageUnitSerializer, ArticleSerializer, GroupSerializer, QRCodeSerializer, OrderSerializer, StorageSpaceSerializer
# This import is important for now, since the dependency in articlemanagmentservice will not be stored in the serviceInjector otherwise however, I'm
# hoping to be able to change this since it looks kind of trashy
from backend.services.articleManagementService import articleManagementService
from backend.services.userService import userService
from backend.services.groupManagementService import groupManagementService
from backend.services.storageManagementService import storageManagementService
from backend.services.orderServices import OrderService
from django.views import View
from backend.__init__ import serviceInjector as si
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
    def __init__(self, _deps, *args):
        self._articleManagementService : articleManagementService = _deps['articleManagementService']()

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
    def __init__(self, _deps, *args):
        self._groupManagementService : groupManagementService = _deps['groupManagementService']()

    def get(self, request, groupId):
        if request.method == 'GET':
            group = self._groupManagementService.getGroupById(groupId)
            if group is None:
                raise Http404("Could not find group")
            serializer = GroupSerializer(group)
    #TODO: I assume that there is supposed to be some type of return here.

class storage(View):
    # Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps, *args):
        self._storageManagementService : storageManagementService = _deps['storageManagementService']()

    def get(self, request, storageId):
        if request.method == 'GET':
            storage = self._storageManagementService.getStorageUnitById(storageId)
            if storage is None:
                raise Http404("Could not find storage")
            serializer = StorageUnitSerializer(storage)
            if serializer.is_valid:
                return JsonResponse(serializer.data, status=200)
            return HttpResponseBadRequest


class storageSpace(View):
    def __init__(self, _deps, *args):
        self._orderService : OrderService = _deps['OrderService']()
        self._storageManagementService : storageManagementService = _deps['storageManagementService']()
    def get(self, request, storageSpaceId):
        alteredDict = self._storageManagementService.getCompartmentContentAndOrders(storageSpaceId)
        if alteredDict is None: 
            return Http404("Could not find storage space")
        return JsonResponse(alteredDict, status=200)


class order(View): 
    @si.inject
    def __init__(self, _deps, *args):
        self._orderService : OrderService = _deps['OrderService']() 
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

            order = self._orderService.place_order_if_no_order(
                storage_unit_id=storageUnit, article_id=article, amount=amount
            )

            serializer = OrderSerializer(order)
            if serializer.is_valid:
                return JsonResponse(serializer.data, status=200)
            return HttpResponseBadRequest

class Login(APIView):
    @si.inject #Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing 
    def __init__(self, _deps, *args):
        self._userService : userService = _deps['userService']()

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
    def __init__(self, _deps, *args):
        self._userService : userService = _deps['userService']()

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


class seeAllStorageUnits(View):
    @si.inject
    def __init__(self, _deps, *args):
        _storageManagementService = _deps['storageManagementService']
        # Instance of dependency is created in constructor
        self._storageManagementService : storageManagementService = _storageManagementService()

    def get(self, request):
        if request.method == 'GET':
            allStorages = self._storageManagementService.getAllStorageUnits()
            if allStorages is None:
                raise Http404("Could not find any storage units")
            else:
                return JsonResponse(list(allStorages), safe=False, status=200)


class AddInputUnit(View):
    @si.inject
    def __init__(self, _deps):
        storageManagementService = _deps['storageManagementService']
        self._storageManagementService = storageManagementService()
        self._storageAccess = storageAccess()
        self._userService: userService = _deps['userService']()

    def post(self, request, storage_space_id, amount):
        storage_space = storageManagementService.getStorageSpaceById(
            self=self, id=storage_space_id)
        user = request.user
        if request.method == 'POST':
            if storage_space == None:
                return Http404("Could not find storage space")
            storageManagementService.addToStorage(self=self,
                                                  space_id=storage_space_id, amount=amount, username=user.username, addOutputUnit=False)
            return HttpResponse(status=200)

# AddOutputUnit is used to add articles to the storage space in
# the form of single articles, or smaller parts etc.
# For example: One output unit could be one single mask or the article -->one meter of paper.
# Creates a transaction


class GetUserTransactions(View):
    @si.inject
    def __init__(self, _deps):
        self._userService : userService = _deps['userService']()
    
    def get(self, request, user_id):
        current_user = User.objects.filter(id=user_id)

        if current_user.exists() == False:
            return Response({'error': 'User ID does not exist'}, status=status.HTTP_404_NOT_FOUND)

        all_transactions_by_user = self._userService.get_all_transactions_by_user(current_user = current_user)
        
        if all_transactions_by_user is None:
            raise Http404("Could not find any transactions")
        else:
            return JsonResponse(list(all_transactions_by_user), safe=False, status = 200)
            
class ReturnUnit(View):
    @si.inject
    def __init__(self, _deps):
        #storageAccess = _deps['storageAccess']
        storageManagementService = _deps['storageManagementService']
        self._storageManagementService = storageManagementService()
        self._storageAccess = storageAccess()
        self._userService: userService = _deps['userService']()

    def post(self, request, storage_space_id, amount):
        storage_space = storageManagementService.getStorageSpaceById(
            self=self, id=storage_space_id)
        user = request.user
        if request.method == 'POST':
            if storage_space == None:
                return Http404("Could not find storage space")
            storageManagementService.addToReturnStorage(
                space_id=storage_space_id, amount=amount, username=user.username, addOutputUnit=True)
            return HttpResponse(status=200)


class getStorageValue(View):
    @si.inject
    def __init__(self, _deps):
        _storageManagementService = _deps['storageManagementService']
        self._storageManagementService: storageManagementService = _storageManagementService()

    def get(self, request, storageId):
        if request.method == 'GET':
            storage = self._storageManagementService.getStorageUnitById(
                storageId)
            if storage is None:
                raise Http404("Could not find storage")
            else:
                value = self._storageManagementService.getStorageValue(
                    storageId)
                return JsonResponse(value, safe=False, status=200)

# Gets alternative articles for a given article. If only article id is entered, the method returns a list of alternative articles and all
# their attributes. If an article id and a storage id is entered, the method returns the id for alternative articles and the amount of
# the alternative articles in that storage


class getArticleAlternatives(View):
    @si.inject
    def __init__(self, _deps):
        _articleManagementService = _deps['articleManagementService']
        # Instance of dependency is created in constructor
        self._storageManagementService: storageManagementService = _deps['storageManagementService'](
        )
        self._articleManagementService: articleManagementService = _articleManagementService()

    def get(self, request, articleId, storageId=None):
        if request.method == 'GET':

            article = self._articleManagementService.getAlternativeArticles(
                articleId)

            if storageId is not None:
                storageList = []
                dict = {'Article: ': None, 'Amount: ': None}
                for i in article:
                    dict['Article: '] = i.lioId
                    dict['Amount: '] = self._storageManagementService.searchArticleInStorage(
                        storageId, i.lioId)
                    storageList.append(dict.copy())

            if article is None:
                raise Http404("Could not find article")
            else:
                if storageId is not None:
                    return JsonResponse(list(storageList), safe=False, status=200)
                else:
                    return JsonResponse(list(article.values()), safe=False, status=200)
