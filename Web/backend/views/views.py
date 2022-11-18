from logging.config import valid_ident
from ..serializers import AlternativeNameSerializer, StorageSerializer, ApiCompartmentSerializer, UserInfoSerializer
from ..serializers import ArticleSerializer, OrderSerializer, OrderedArticleSerializer
from ..serializers import CompartmentSerializer, TransactionSerializer
from ..serializers import GroupSerializer

from backend.services.articleManagementService import ArticleManagementService
from backend.services.userService import UserService
from backend.services.groupManagementService import GroupManagementService
from backend.services.storageManagementService import StorageManagementService
from backend.services.orderServices import OrderService

from backend.__init__ import serviceInjector as si
from django.views import View
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
# from rest_framework.decorators import renderer_classes, api_view
from django.http import HttpResponse
from itertools import chain
from operator import itemgetter
from backend.coremodels.compartment import Compartment
from django.http import HttpResponse
from datetime import date
from datetime import datetime
import datetime
from django.utils.timezone import now

# from Web.backend import serializers


class Article(View):
    '''Article view.'''

    # Dependencies are injected, I hope that we will be able to mock
    # (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps, *args):
        self.article_management_service: ArticleManagementService = (
            _deps['ArticleManagementService']())

    def get(self, request, article_id):
        '''Get.'''
        if request.method == 'GET':
            # A user can get articles if they have permission
            if not request.user.has_perm('backend.view_article'):
                raise PermissionDenied
            article = self.article_management_service.get_article_by_lio_id(
                article_id)
            supplier = self.article_management_service.get_supplier(article)
            supplier_article_nr = (
                self.article_management_service.get_supplier_article_nr(
                    article))
            compartments = list(article.compartment_set.all())
            alternative_names = list(article.alternativearticlename_set.all())

            if article is None:
                raise Http404("Could not find article")

            serializer = ArticleSerializer(article)

            compartment_list = []
            unit_list = []
            for i in compartments:
                compartment_serializer = CompartmentSerializer(i)
                unit_serializer = StorageSerializer(i.storage)

                compartment_list.append(compartment_serializer.data)
                unit_list.append(unit_serializer.data.get('name'))

            alt_names_list = []
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


class Group(View):
    '''Group.'''
    # Dependencies are injected, I hope that we will be able to mock
    # (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps, *args):
        self.group_management_service: GroupManagementService = (
            _deps['GroupManagementService']())

    def get(self, request, groupId):
        '''Get.'''
        if request.method == 'GET':
            # A user can see a group if they have permission
            if not request.user.has_perm('backend.view_group'):
                raise PermissionDenied
            group = self.group_management_service.get_group_by_id(groupId)
            if group is None:
                raise Http404("Could not find group")
            serializer = GroupSerializer(group)
    # TODO: I assume that there is supposed to be some type of return here.


class Storage(View):
    '''Storage view.'''
    # Dependencies are injected, I hope that we will be able to mock
    # (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps, *args):
        self.storage_management_service: StorageManagementService = (
            _deps['StorageManagementService']())

    def get(self, request, storage_id):
        '''Return storage unit using id.'''
        if request.method == 'GET':
            # A user can see a storage if they have permission
            if not request.user.has_perm('backend.view_storage'):
                raise PermissionDenied
            storage = (
                self.storage_management_service.get_storage_by_id(
                    storage_id))

            compartments = self.storage_management_service.get_compartment_by_storage_id(
                storage_id)
            data = {}
            data['id'] = storage.id
            data['location'] = {'building': storage.building,
                                'floor': storage.floor}
            serialized_compartments = []
            for compartment in compartments:
                serialized_compartments.append(
                    CompartmentSerializer(compartment).data)
            data['compartments'] = serialized_compartments
            if storage is None:
                raise Http404("Could not find storage")
            #serializer = StorageSerializer(storage)
            # if serializer.is_valid:
            return JsonResponse(data, status=200, safe=False)
            return HttpResponseBadRequest


class NearbyStorages(View):
    '''Get nearby storages.'''
    @si.inject
    def __init__(self, _deps, *args):
        self.storage_management_service: StorageManagementService = (
            _deps['StorageManagementService']())

    def get(self, request, qr_code):
        '''Return nearby storages of the storage which
        contains the qr_code with a
        specific qr_code'''
        if request.method == 'GET':
            nearby_storages = (
                self.storage_management_service.get_nearby_storages(qr_code))
            if nearby_storages is None:
                raise Http404("Could not find any nearby storages")

            serializer = []
            for key_storage in nearby_storages:
                possible_storage = {}
                possible_storage['id'] = key_storage.id
                possible_storage['location'] = {
                    'building': key_storage.building,
                    'floor': key_storage.floor}
                possible_storage['compartment'] = (
                    CompartmentSerializer(nearby_storages[key_storage]).data)
                serializer.append(possible_storage)
                valid = True
            if valid:
                return JsonResponse(list(serializer), status=200, safe=False)
            return HttpResponseBadRequest


class Compartments(APIView):
    '''Compartment view.'''
    # Dependencies are injected, I hope that we will be able to mock
    # (i.e. make stubs of) these for testing
    @si.inject
    def __init__(self, _deps, *args):
        self.storage_management_service: StorageManagementService = (
            _deps['StorageManagementService']())

    def get(self, request, qr_code):
        '''Returns compartment using qr code.'''
        if request.method == 'GET':
            # A user can see compartments if they have permission
            if not request.user.has_perm('backend.view_compartment'):
                raise PermissionDenied
            compartment = (
                self.storage_management_service.get_compartment_by_qr(
                    qr_code))
            if compartment is None:
                return Http404("Could not find compartment")
            else:
                serializer = CompartmentSerializer(compartment)
                if serializer.is_valid:
                    return JsonResponse(serializer.data, status=200)
                return HttpResponseBadRequest

    def post(self, request):
        '''Post compartment.'''
        if request.method == 'POST':
            # A user can add a compartment if they have permission
          #          if not request.user.has_perm('backend.add_compartment'):
           #             raise PermissionDenied
            json_body = request.data
            storage_id = json_body['storageId']
            placement = json_body['placement']
            qr_code = json_body['qrCode']
            compartment = self.storage_management_service.create_compartment(
                storage_id, placement, qr_code
            )

        serializer = CompartmentSerializer(compartment)
        if serializer.is_valid:
            return JsonResponse(serializer.data, status=200)
        return HttpResponseBadRequest


class Order(APIView):
    '''Order endpoint handling all request from /orders'''
    @si.inject
    def __init__(self, _deps, *args):
        self.order_service: OrderService = _deps['OrderService']()
        self.article_management_service: ArticleManagementService = _deps['ArticleManagementService'](
        )

    def get(self, request):
        '''Returns all orders)'''
        # A user can view orders if they have permission
        if not request.user.has_perm('backend.view_order'):
            raise PermissionDenied

        orders = self.order_service.get_orders()
        ordered_articles = self.order_service.get_all_ordered_articles()

        serialized_articles = []
        for ordered_article in ordered_articles:
            real_article = self.article_management_service.get_article_by_lio_id(
                ordered_article.article.lio_id)
            print(ordered_article)
            serialized_article = ArticleSerializer(real_article)
            serialized_order_article = OrderedArticleSerializer(
                ordered_article)
            serialized_articles.append(serialized_article.data)
            serialized_articles.append(serialized_order_article.data)
            if ordered_article is None:
                return HttpResponseBadRequest

        for order in orders:
            serialized_order = OrderSerializer(order)

            if serialized_order.is_valid:
                data = {}
                data.update(serialized_order.data)
                data['articles'] = serialized_articles
                return Response(data, status=200)
            return HttpResponseBadRequest

    def post(self, request, format=None):
        '''Places an order'''
        if request.method == 'POST':
            # A user can add an order if they have permission for it
            #            if not request.user.has_perm('backend.add_order'):
         #               raise PermissionDenied
            json_body = request.data
            storage_id = json_body['storageId']
            ordered_articles = json_body['articles']

            max_wait = 0
            for ordered_article in ordered_articles:
                temp = self.order_service.calculate_expected_wait(
                    article_id=ordered_article['lioNr'], amount=ordered_article['quantity'])
                if (temp > max_wait):
                    max_wait = temp

            estimated_delivery_date = datetime.datetime.now() + \
                datetime.timedelta(days=max_wait)

            order = self.order_service.place_order(
                storage_id=storage_id, estimated_delivery_date=estimated_delivery_date, ordered_articles=ordered_articles)

            if order is None:
                return HttpResponseBadRequest

            for ordered_article in ordered_articles:
                OrderService.create_ordered_article(
                    ordered_article['lioNr'], ordered_article['quantity'], ordered_article['unit'], order)
            serialized_order = OrderSerializer(order)
            if serialized_order.is_valid:
                return Response(serialized_order.data, status=200)
            return HttpResponseBadRequest


class OrderId(APIView):
    '''Order Endpoint which handles all request coming from /orders/id'''
    @si.inject
    def __init__(self, _deps, *args):
        self.order_service: OrderService = _deps['OrderService']()
        self.article_management_service: ArticleManagementService = _deps['ArticleManagementService'](
        )

    def get(self, request, id):
        order = self.order_service.get_order_by_id(id)
        print(order)
        if order is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serialized_order = OrderSerializer(order)
        if serialized_order.is_valid:
            return Response(serialized_order.data, status=200)
        return HttpResponseBadRequest

    def put(self, request, id):
        '''OBS! Not yet finished! Only used for testing. Written by Hugo and Jakob. 
        Alters the state of an order to delivered and updates the amount in the correct compartments.'''
        json_body = request.data
        order_state = json_body['state']

        if order_state == "delivered":
            updated_order = self.order_service.order_arrived(id)

        if updated_order is None:
            return HttpResponseBadRequest

        serialized_order = OrderSerializer(updated_order)
        if serialized_order.is_valid:
            return Response(serialized_order.data, status=200)
        return HttpResponseBadRequest

    def delete(self, request, id):
        '''Delete order func'''
        deleted_order = self.order_service.delete_order(id)
        if deleted_order is None:
            return HttpResponseBadRequest
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginWithCredentials(APIView):
    '''Login a user using credentials username and password and returns
    the user along with bearer auth token'''
    @si.inject
    def __init__(self, _deps, *args):
        self.user_service: UserService = _deps['UserService']()

    def post(self, request):
        '''Login a user using credentials username and password. 
        returns User along with auth token'''
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Authorization information is missing or invalid'},
                            status=status.HTTP_401_UNAUTHORIZED)

        auth = authenticate(username=username, password=password)
        if auth is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        login(request, auth)

        token = self.user_service.create_auth_token(request)
        if token is None:
            return HttpResponseBadRequest

        user = self.user_service.get_user_info(request.user)
        serialized_user = UserInfoSerializer(user)
        data = {
            "user:": serialized_user.data,
            "token:": token
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class LoginWithBarcodeOrNfc(APIView):
    '''Login a user using either barcode or NFC to authenticate user.
    Returns the user along with bearer auth token'''
    @si.inject
    def __init__(self, _deps, *args):
        self.user_service: UserService = _deps['UserService']()

    def post(self, request):
        '''Login a user using either barcode or NFC.
        returns User along with auth token'''
        # body = request.data
        barcode_id = request.data.get('barcodeId')
        nfc_id = request.data.get('nfcId')
        if barcode_id is None and nfc_id is None:
            return Response({'error': 'Authorization information is missing or invalid'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if barcode_id is not None:
            user = self.user_service.get_user_with_barcode(
                barcode_id=barcode_id)
        elif nfc_id is not None:
            user = self.user_service.get_user_with_nfc(nfc_id=nfc_id)

        if user is None:
            return Response({'error': 'Authorization information is missing or invalid'},
                            status=status.HTTP_401_UNAUTHORIZED)

        auth = user.user

        login(request, auth)
        token = self.user_service.create_auth_token(request)
        if token is None:
            return HttpResponseBadRequest

        serialized_user = UserInfoSerializer(user)
        data = {
            "user:": serialized_user.data,
            "token:": token
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class SeeAllStorages(View):
    '''See all storages view.'''
    @si.inject
    def __init__(self, _deps, *args):
        storage_management_service = _deps['StorageManagementService']
        # Instance of dependency is created in constructor
        self.storage_management_service: StorageManagementService = (
            storage_management_service())

    def get(self, request):
        '''Returns all storages.'''
        if request.method == 'GET':
            # A user can see all storages if they have permission
            if not request.user.has_perm('backend.view_storage'):
                raise PermissionDenied
            all_storages = self.storage_management_service.get_all_storages()
            if all_storages is None:
                raise Http404("Could not find any storage units")
            else:
                serialized_storages = []
                for storage in all_storages:
                    data = {}
                    data['id'] = storage["id"]
                    data['location'] = {'building': storage["building"],
                                        'floor': storage["floor"]}
                    compartments = self.storage_management_service.get_compartment_by_storage_id(
                        storage["id"])
                    serialized_compartments = []
                    for compartment in compartments:
                        serialized_compartments.append(
                            CompartmentSerializer(compartment).data)
                    data['compartments'] = serialized_compartments
                    serialized_storages.append(data)

                print(serialized_storages)
                return JsonResponse(serialized_storages, status=200, safe=False)

            # return JsonResponse(list(all_storages), safe=False, status=200)


class AddInputUnit(View):
    '''Add input unit view.'''
    @si.inject
    def __init__(self, _deps):
        self.storage_management_service = _deps['StorageManagementService']
        self.user_service: UserService = _deps['UserService']()

    def post(self, request, compartment_id, amount, time_of_transaction):
        '''Post addition to storage.'''
        # Custom permission to be able to add a input unit. Can be found in the coremodel storage.py
        if not request.user.has_perm('backend.add_input_unit'):
            raise PermissionDenied
        compartment = StorageManagementService.get_compartment_by_id(
            self=self, id=compartment_id)
        user = request.user
        if request.method == 'POST':
            if compartment is None:
                return Http404("Could not find storage space")
            StorageManagementService.add_to_storage(self=self,
                                                    id=compartment_id,
                                                    amount=amount,
                                                    username=user.username,
                                                    add_output_unit=False,
                                                    time_of_transaction=(
                                                        time_of_transaction))
            return HttpResponse(status=200)

# AddOutputUnit is used to add articles to the storage space in
# the form of single articles, or smaller parts etc.
# For example: One output unit could be one single mask or
# the article -->one meter of paper.
# Creates a transaction


class GetUserTransactions(View):
    '''Get user transactions view.'''
    @si.inject
    def __init__(self, _deps):
        self.user_service: UserService = _deps['UserService']()

    def get(self, request, user_id):
        '''Returns all transactions made by user.'''
        # Custom permission to be able to see a users transactions. Can be found in the coremodel transaction.py
        if not request.user.has_perm('backend.get_user_transactions'):
            raise PermissionDenied
        current_user = User.objects.filter(id=user_id)

        if current_user is not None:
            all_transactions_by_user = (
                self.user_service.get_all_transactions_by_user(
                    current_user=current_user))

            if all_transactions_by_user is not None:
                return JsonResponse(list(all_transactions_by_user),
                                    safe=False, status=200)
            else:  # Exception
                return Response({'error': 'Could not find any transactions'},
                                status=status.HTTP_404_NOT_FOUND)
        else:  # Exception
            return Response({'error': 'Could not find user'},
                            status=status.HTTP_404_NOT_FOUND)


class ReturnUnit(View):
    '''Return unit view.'''
    @si.inject
    def __init__(self, _deps):
        self.storage_management_service = _deps['StorageManagementService']
        self.user_service: UserService = _deps['UserService']()

    def post(self, request, compartment_id, amount, time_of_transaction=now):
        '''Post return to storage.'''
        # A user can return to storage if they have permission
        if not request.user.has_perm('backend.return_to_storage'):
            raise PermissionDenied
        compartment = StorageManagementService.get_compartment_by_id(
            self=self, id=compartment_id)
        user = request.user
        if request.method == 'POST':
            if compartment is None:
                return Http404("Could not find storage space")
            StorageManagementService.add_to_return_storage(
                self=self,
                id=compartment_id,
                amount=amount,
                username=user.username,
                add_output_unit=True,
                time_of_transaction=(
                    time_of_transaction))
            return HttpResponse(status=200)


class Transactions(APIView):
    '''Transactions API view.'''
    @si.inject
    def __init__(self, _deps):
        self.user_service: UserService = _deps['UserService']()
        self.storage_management_service: StorageManagementService = (
            _deps['StorageManagementService']())

    def get(self, request):
        '''Get all transactions.'''
        if request.method == 'GET':
            # Custom permission to be able to see all transactions. Can be found in the coremodel transaction.py
            if not request.user.has_perm('backend.get_all_transaction'):
                raise PermissionDenied
            all_transactions = (
                self.storage_management_service.get_all_transactions())
        if all_transactions is None:
            raise Http404("Could not find any transactions")
        else:
            return JsonResponse(list(all_transactions), safe=False, status=200)

    def post(self, request):
        '''Description needed.'''
        if not request.user.has_perm('backend.add_transaction'):
            raise PermissionDenied
        compartment = self.storage_management_service.get_compartment_by_qr(
            qr_code=request.data.get("qrCode"))
        if compartment is None:
            return Response({'error': 'Could not find compartment'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            storage = self.storage_management_service.get_storage_by_id(
                id=compartment.id)
            amount = request.data.get("quantity")
            unit = request.data.get("unit")
            user = request.user
            operation = request.data.get("operation")
            time_of_transaction = request.data.get("time_of_transaction")

            if time_of_transaction == "" or time_of_transaction is None:
                time_of_transaction = date.today()

            if unit == "output":
                add_output_unit = False
            else:
                add_output_unit = True

            if operation == "replenish":
                transaction = self.storage_management_service.add_to_storage(
                    id=compartment.id, amount=amount,
                    username=user.username, add_output_unit=add_output_unit,
                    time_of_transaction=time_of_transaction)
                return JsonResponse(TransactionSerializer(transaction).data,
                                    status=200)
            elif operation == "return":
                transaction = (
                    self.storage_management_service.add_to_return_storage(
                        id=compartment.id, amount=amount,
                        username=user.username,
                        add_output_unit=add_output_unit,
                        time_of_transaction=time_of_transaction))
                return JsonResponse(TransactionSerializer(transaction).data,
                                    status=200)
            elif operation == "takeout":
                transaction = (
                    self.storage_management_service.take_from_Compartment(
                        id=compartment.id, amount=amount,
                        username=user.username,
                        add_output_unit=add_output_unit,
                        time_of_transaction=time_of_transaction))
                return JsonResponse(TransactionSerializer(transaction).data,
                                    status=200)
            elif operation == "adjust":
                transaction = (
                    self.storage_management_service.set_compartment_amount(
                        compartment_id=compartment.id, amount=amount,
                        username=user.username,
                        add_output_unit=add_output_unit,
                        time_of_transaction=time_of_transaction))
                return JsonResponse(TransactionSerializer(transaction).data,
                                    status=200)


class TransactionsById(APIView):
    '''Get transaction by ID view.'''
    @si.inject
    def __init__(self, _deps):
        StorageManagementService = _deps['StorageManagementService']
        self.storage_management_service = StorageManagementService()
        self.user_service: UserService = _deps['UserService']()

    def get(self, request, transaction_id):
        '''Get transaction.'''
        if request.method == 'GET':
            # Custom permission to be able to get transactiopns by id. Can be found in the coremodel transaction.py
            if not request.user.has_perm('backend.get_transaction_by_id'):
                raise PermissionDenied
            transaction = (
                self.storage_management_service.get_transaction_by_id(transaction_id))
        if transaction is None:
            raise Http404("Could not find the transaction")
        else:
            return JsonResponse(TransactionSerializer(transaction).data, safe=False, status=200)

    def put(self, request, transaction_id):
        '''Put transaction.'''
        if request.method == 'PUT':
            # Can only change a transaction if they have the permission
            if not request.user.has_perm('backend.change_transaction'):
                raise PermissionDenied
            new_time_of_transaction = request.data.get("time_of_transaction")
            transaction = (
                self.storage_management_service.edit_transaction_by_id(transaction_id, new_time_of_transaction))

        if transaction is None:
            raise Http404("Could not find the transaction")
        else:
            return JsonResponse(TransactionSerializer(transaction).data, safe=False, status=200)


class GetStorageValue(View):
    '''Get storage value view.'''
    @si.inject
    def __init__(self, _deps):
        storage_management_service = _deps['StorageManagementService']
        self.storage_management_service: StorageManagementService = (
            storage_management_service())

    def get(self, request, storage_id):
        '''Get storage unit value using id.'''
        if request.method == 'GET':
            # Custom permission to be able to see storage value. Can be found in the coremodel storage.py
            if not request.user.has_perm('backend.get_storage_value'):
                raise PermissionDenied
            storage = self.storage_management_service.get_storage_by_id(
                storage_id)
            if storage is None:
                raise Http404("Could not find storage")
            else:
                value = self.storage_management_service.get_storage_value(
                    storage_id)
                return JsonResponse(value, safe=False, status=200)


class GetStorageCost(APIView):
    '''Get storage cost API view.'''
    @si.inject
    def __init__(self, _deps, *args):
        storage_management_service = _deps['StorageManagementService']
        self.storage_management_service: StorageManagementService = (
            storage_management_service())

    def get(self, request, storage_id):
        '''Get storage cost.'''
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        if request.method == 'GET':
            # Custom permission to be able to see storage cost. Can be found in the coremodel storage.py
            if not request.user.has_perm('backend.get_storage_cost'):
                raise PermissionDenied
            storage = self.storage_management_service.get_storage_by_id(
                storage_id)
            if storage is None:
                raise Http404("Could not find storage")
            else:
                value = self.storage_management_service.get_storage_cost(
                    storage_id, start_date, end_date)
            return JsonResponse(value, safe=False, status=200)

# Gets alternative articles for a given article. If only article id
# is entered, the method returns a list of alternative articles and all
# their attributes. If an article id and a storage id is entered, the
# method returns the id for alternative articles and the amount of
# the alternative articles in that storage


class GetArticleAlternatives(View):
    '''Get alternative article view. Gets alternative articles for a
       given article. If only article id
       is entered, the method returns a list of alternative articles and all
       their attributes. If an article id and a storage id is entered, the
       method returns the id for alternative articles and the amount of
       the alternative articles in that storage'''
    @si.inject
    def __init__(self, _deps):
        article_management_service = _deps['ArticleManagementService']
        # Instance of dependency is created in constructor
        self.storage_management_service: StorageManagementService = (
            _deps['StorageManagementService']())
        self.article_management_service: ArticleManagementService = (
            article_management_service())

    def get(self, request, article_id, storage_id=None):
        '''Get.'''
        if request.method == 'GET':
            # If a user can view articles, then they can get their alternative articles
            if not request.user.has_perm('backend.view_article'):
                raise PermissionDenied
            article = self.article_management_service.get_alternative_articles(
                article_id)

            if storage_id is not None:
                storage_list = []
                dict = {'Article: ': None, 'Amount: ': None}
                for i in article:
                    dict['Article: '] = i.lio_id
                    dict['Amount: '] = (
                        self.storage_management_service.search_article_in_storage(
                            storage_id, i.lio_id))
                    storage_list.append(dict.copy())

            if article is None:
                raise Http404("Could not find article")
            else:
                if storage_id is not None:
                    return JsonResponse(list(storage_list),
                                        safe=False,
                                        status=200)
                else:
                    return JsonResponse(list(article.values()),
                                        safe=False,
                                        status=200)


# FR 8.1 start #
class SearchForArticleInStorages(View):
    '''Search for article in storages view.'''
    @si.inject
    def __init__(self, _deps):
        OrderService = _deps['OrderService']
        UserService = _deps['UserService']
        self._storage_management_service = _deps['StorageManagementService']
        self._user_service = UserService()
        self._order_service = OrderService()

    def get(self, request, search_string, input_storage) -> dict:
        '''Return articles in a given storage which matches
           Search.'''
        if request.method == 'GET':
            # If a user has permission to view articles, then they can search for them
            if not request.user.has_perm('backend.view_article'):
                raise PermissionDenied
            # Getting the storage unit which is connected
            # to the users cost center.
            user = request.user
            user_info = self._user_service.get_user_info(user.id)
            user_storage = (
                self._storage_management_service.get_storage_by_costcenter(
                    user_info.cost_center))

            # If not input storage unit is given, we assume the user wants to
            # search from it's own storage unit
            if input_storage is None:
                storage = user_storage.id
            else:
                storage = input_storage

            # NOTE: In order to increase testability and reusability I would
            # like to see already existing functions in
            # the service- / data access layer being used here. Another tip is
            # to query the "articles" variable
            # based on storage_id != storage (then duplicates will not
            # have to be removed)

            # query for the articles which match the input search string
            # and the chosen storage unit.
            articles_in_chosen_storage = Compartment.objects.filter(
                article__name__contains=search_string,
                storage_unit__id=storage).values_list(
                'article__name', 'id', 'amount', 'storage_unit__name',
                'storage_unit__floor', 'storage_unit__building')
            # query for the articles which only matches the input search
            # string in all storage units.
            articles = Compartment.objects.filter(
                article__name__contains=search_string).values_list(
                'article__name', 'id', 'amount', 'storage_unit__name',
                'storage_unit__floor', 'storage_unit__building')

            # sort the articles which does not match with
            # the chosen storage unit.
            sorted_articles = sorted(
                list(articles), key=itemgetter(5, 4))

            # chain the querysets together.
            data = list(chain(articles_in_chosen_storage, sorted_articles))

            # ugly way to remove duplicates from the data. Can't use set()
            # since order has to be preserved
            data2 = []
            for article in data:
                if article not in data2:
                    data2.append(article)

            return JsonResponse(data2, safe=False, status=200)


class ArticleToCompartmentByQRcode(APIView):
    '''Change Article linked to Compartment by using QR code.'''
    @si.inject
    def __init__(self, _deps):
        self.storage_management_service: StorageManagementService = (
            _deps['StorageManagementService']())
        self.article_management_service: ArticleManagementService = (
            _deps['ArticleManagementService']())

    def post(self, request, qr_code):
        '''Sets new article in payload to compartment matching qr_code.'''

        current_compartment = (
            self.storage_management_service.get_compartment_by_qr(
                qr_code=qr_code))

        if current_compartment is not None:
            article_id = request.data.get("lioNr")
            new_article = (
                self.article_management_service.get_article_by_lio_id((
                    article_id)))

            if new_article is not None:
                # Get attributes from payload
                new_amount = request.data.get("quantity")
                new_standard_order_amount = request.data.get(
                    ("normalOrderQuantity"))
                new_order_point = request.data.get("orderQuantityLevel")

                # Updates attributes in compartment
                self.storage_management_service.update_compartment(
                    current_compartment, new_article, new_amount, new_standard_order_amount, new_order_point)

                return JsonResponse(ApiCompartmentSerializer
                                    (current_compartment).data)
            else:  # Exception
                return Response({'error': 'Could not find article'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:  # Exception
            return Response({'error': 'Could not find compartment'},
                            status=status.HTTP_400_BAD_REQUEST)


class getEconomy(APIView):
    '''Returns the total value in storage, and the average turnover rate'''
    @si.inject
    def __init__(self, _deps, *args):
        storage_management_service = _deps['StorageManagementService']
        self.storage_management_service: StorageManagementService = (
            storage_management_service())

    def get(self, request, storage_id):
        '''Takes the storage_id from the url'''
        storage = self.storage_management_service.get_storage_by_id(
            storage_id)
        if storage is None:
            raise Http404("Could not find storage")
        else:
            start_date = '2022-01-01'
            end_date = '2022-12-31'
            '''Below is not an average value, but the current value right now since 
            get_storage_value doesn't take transactions into account'''
            value = self.storage_management_service.get_storage_value(
                storage_id)
            cost = self.storage_management_service.get_storage_cost(
                storage_id, start_date, end_date)
            data = {}
            data["totalValue"] = value
            data["averageTurnoverRate"] = int((value/cost)*365)
            return JsonResponse(data, safe=False, status=200)


class MoveArticle(APIView):
    '''Move an amount of a specific article from one compartment to another one.
        This will create two transactions, one for the withdrawal and one for the deposit.'''
    @si.inject
    def __init__(self, _deps, *args):
        storage_management_service = _deps['StorageManagementService']
        self.storage_management_service: StorageManagementService = (
            storage_management_service())
        self.user_service: UserService = _deps['UserService']()

    def post(self, request):
        data = request.data.get
        from_compartment_qr_code = data('fromCompartmentQrCode')
        to_compartment_qr_code = data('toCompartmentQrCode')
        unit = data('unit')
        quantity = data('quantity')
        user = request.user

        if request.method == 'POST':

            from_compartment = self.storage_management_service.get_compartment_by_qr(
                from_compartment_qr_code)
            to_compartment = self.storage_management_service.get_compartment_by_qr(
                to_compartment_qr_code)

            if from_compartment is None or to_compartment is None:
                return Response({'error': 'Could not find compartment'},
                                status=status.HTTP_400_BAD_REQUEST)

            if (from_compartment.amount-quantity) < 0:
                return Response({'error': 'Not enough articles in compartment'},
                                status=status.HTTP_400_BAD_REQUEST)

            if from_compartment.article.lio_id != to_compartment.article.lio_id:
                return Response({'error': 'Not matching articles'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                if unit == "output":
                    add_output_unit = False
                else:
                    add_output_unit = True

                time_of_transaction = date.today()

                from_transaction = (
                    self.storage_management_service.take_from_Compartment(
                        id=from_compartment_qr_code, amount=quantity,
                        username=user.username,
                        add_output_unit=add_output_unit,
                        time_of_transaction=time_of_transaction))

                to_transaction = (
                    self.storage_management_service.add_to_return_storage(
                        id=to_compartment_qr_code, amount=quantity,
                        username=user.username,
                        add_output_unit=add_output_unit,
                        time_of_transaction=time_of_transaction))
                '''Prints JsonResponse directly instead of using Serializer'''
                data = {}
                '''Id of the transaction created when takeout'''
                data['id'] = str(from_transaction.id)
                data['userId'] = str(user.id)
                data['timeStamp'] = time_of_transaction
                data['fromCompartmentQrCode'] = from_compartment_qr_code
                data['toCompartmentQrCode'] = to_compartment_qr_code
                data['lioNr'] = from_compartment.article.lio_id
                data['unit'] = unit
                data['qunatity'] = quantity

                return JsonResponse(data, safe=False, status=200)
