from http.client import OK, HTTPResponse
from itertools import chain
from operator import itemgetter
import pkgutil
from urllib import request
import json
from django.shortcuts import render
from rest_framework import generics
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from backend.coremodels.transaction import Transaction
from backend.dataAccess.storageAccess import storageAccess
from ..serializers import AlternativeNameSerializer, StorageUnitSerializer, ArticleSerializer, GroupSerializer, QRCodeSerializer, OrderSerializer, StorageSpaceSerializer, TransactionSerializer
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
from rest_framework.decorators import renderer_classes, api_view
from django.http import HttpResponse
from itertools import chain

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
            supplier = self._articleManagementService.getSupplier(article)
            supplier_article_nr = self._articleManagementService.getSupplierArticleNr(
                article)
            compartments = list(article.storagespace_set.all())
            alternative_names = list(article.alternativearticlename_set.all())

            if article is None:
                raise Http404("Could not find article")

            serializer = ArticleSerializer(article)

            compartment_list = []
            unit_list = []
            for i in compartments:
                compartment_serializer = StorageSpaceSerializer(i)
                unit_serializer = StorageUnitSerializer(i.storage_unit)

                compartment_list.append(compartment_serializer.data)
                unit_list.append(unit_serializer.data.get('name'))

            alt_names_list = []
            print(alternative_names)
            for j in alternative_names:
                alternative_names_serializer = AlternativeNameSerializer(j)
                alt_names_list.append(
                    alternative_names_serializer.data.get("name"))

            if serializer.is_valid:
                serializer_data = {}
                serializer_data.update(serializer.data)
                serializer_data["supplier"] = supplier.name
                serializer_data["supplierArticleNr"] = supplier_article_nr
                serializer_data["compartments"] = compartment_list
                serializer_data["units"] = unit_list
                serializer_data["alternative names"] = alt_names_list

                return JsonResponse(serializer_data, safe=False, status=200)
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


class Compartment(View):
    # Dependencies are injected, I hope that we will be able to mock (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps, *args):
        self._storageManagementService: storageManagementService = _deps['storageManagementService'](
        )

    def get(self, request, qr_code):
        print("lets get it")
        if request.method == 'GET':
            compartment = self._storageManagementService.get_compartment_by_qr(
                qr_code)
            if compartment is None:
                return Http404("Could not find compartment")
            else:
                serializer = StorageSpaceSerializer(compartment)
                if serializer.is_valid:
                    return JsonResponse(serializer.data, status=200)
                return HttpResponseBadRequest

    def post(self, request):
        if request.method == 'POST':
            json_body = request.POST

            storage_id = json_body['storage_id']
            placement = json_body['placement']
            qr_code = json_body['qr_code']
            compartment = self._storageManagementService.create_compartment(
                storage_id, placement, qr_code
            )

        serializer = StorageSpaceSerializer(compartment)
        if serializer.is_valid:
            return JsonResponse(serializer.data, status=200)
        return HttpResponseBadRequest


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

class Transactions(APIView):
    @si.inject
    def __init__(self, _deps):
        storageManagementService = _deps['storageManagementService']
        self._storageManagementService = storageManagementService()
        self._storageAccess = storageAccess()
        self._userService: userService = _deps['userService']()

    def get(self, request):
        if request.method == 'GET':
            allTransactions = self._storageManagementService.getAllTransactions()
        if allTransactions is None:
            raise Http404("Could not find any transactions")
        else:          
            return JsonResponse(list(allTransactions), safe=False, status=200)
    
    def post(self, request):
        compartment = self._storageManagementService.get_compartment_by_qr(qr_code=request.data.get("qrCode"))
        if compartment == None:
            return Response({'error': 'Could not find compartment'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            storage = self._storageManagementService.getStorageUnitById(id=compartment.id)
            amount = request.data.get("quantity")
            unit = request.data.get("unit")
            user = request.user
            operation = request.data.get("operation")

            if unit=="output":
                addOutputUnit = False
            else:
                addOutputUnit = True
            
            if operation=="replenish":
                print("printing username")
                print(user)
                transaction = self._storageManagementService.addToStorage(
                    space_id=compartment.id, amount=amount, username=user.username, addOutputUnit=addOutputUnit)
                return JsonResponse(TransactionSerializer(transaction).data, status=200)
            elif operation=="return":
                transaction = self._storageManagementService.addToReturnStorage(
                    space_id=compartment.id, amount=amount, username=user.username, addOutputUnit=addOutputUnit)
                return JsonResponse(TransactionSerializer(transaction).data, status=200)
            elif operation=="takeout":
                transaction = self._storageManagementService.takeFromCompartment(
                    space_id=compartment.id, amount=amount, username=user.username, addOutputUnit=addOutputUnit)
                return JsonResponse(TransactionSerializer(transaction).data, status=200)

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


class getStorageCost(APIView):
    @si.inject
    def __init__(self, _deps, *args):
        _storageManagementService = _deps['storageManagementService']
        self._storageManagementService: storageManagementService = _storageManagementService()

    def get(self, request, storageId):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        if request.method == 'GET':
            storage = self._storageManagementService.getStorageUnitById(
                storageId)
            if storage is None:
                raise Http404("Could not find storage")
            else:
                value = self._storageManagementService.getStorageCost(
                    storageId, start_date, end_date)
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


# FR 8.1 start #
class SearchForArticleInStorages(View):
    @si.inject
    def __init__(self, _deps):
        storageManagementService = _deps['storageManagementService']
        OrderService = _deps['OrderService']
        userService = _deps['userService']
        self._storage_management_service = storageManagementService()
        self._user_service = userService()
        self._order_service = OrderService()

    def get(self, request, search_string, input_storage) -> dict:
        if request.method == 'GET':

            # Getting the storage unit which is connected to the users cost center.
            user = request.user
            user_info = self._user_service.get_user_info(user.id)
            user_storage = self._storage_management_service.get_storage_by_costcenter(
                user_info.cost_center)

            # If not input storage unit is given, we assume the user wants to search from it's own storage unit
            if input_storage is None:
                storage = user_storage.id
            else:
                storage = input_storage

            #NOTE: In order to increase testability and reusability I would like to see already existing functions in 
            # the service- / data access layer being used here. Another tip is to query the "articles" variable
            # based on storage_unit_id != storage (then duplicates will not have to be removed) 

            # query for the articles which match the input search string and the chosen storage unit.
            articles_in_chosen_storage = StorageSpace.objects.filter(article__name__contains=search_string, storage_unit__id=storage).values_list(
                'article__name', 'id', 'amount', 'storage_unit__name', 'storage_unit__floor', 'storage_unit__building')
            # query for the articles which only matches the input search string in all storage units.
            articles = StorageSpace.objects.filter(article__name__contains=search_string).values_list(
                'article__name', 'id', 'amount', 'storage_unit__name', 'storage_unit__floor', 'storage_unit__building')

            # sort the articles which does not match with the chosen storage unit.
            sorted_articles = sorted(
                list(articles), key=itemgetter(5, 4))

            # chain the querysets together.
            data = list(chain(articles_in_chosen_storage, sorted_articles))

            # ugly way to remove duplicates from the data. Can't use set() since order has to be preserved
            data2 = []
            for article in data:
                if article not in data2:
                    data2.append(article)

            return JsonResponse(data2, safe=False, status=200)
