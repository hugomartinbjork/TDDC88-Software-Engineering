from dataclasses import field
from unittest import mock
from rest_framework import serializers
from django.db.models import Q, Case, When, Value, IntegerField

from django.contrib.auth.models import User
from backend.coremodels.alternative_article_name import AlternativeArticleName
from backend.coremodels.article_has_supplier import ArticleHasSupplier
from backend.coremodels.cost_center import CostCenter
from backend.coremodels.article import Article
from backend.coremodels.article import GroupInfo
from backend.coremodels.storage import Storage
from backend.coremodels.cost_center import CostCenter
from backend.coremodels.user_info import UserInfo
from backend.coremodels.compartment import Compartment
from backend.coremodels.order import Order
from backend.coremodels.transaction import Transaction
from backend.coremodels.ordered_article import OrderedArticle
from backend.coremodels.inputOutput import InputOutput



class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('id', 'name')

class UserInfoSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='user_id')
    username = serializers.CharField(source='user')
    role = serializers.CharField(source='group')
    # For some reason this works.
    costCenters = cost_center = CostCenterSerializer(many=True)
    class Meta:
        model = UserInfo
        fields = ('userId', 'username', 'cost_center', 'costCenters', 'role')


class CompartmentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(many=False, read_only=True)
    storageId = serializers.CharField(source='storage_id')
    normalOrderQuantity = serializers.CharField(source='standard_order_amount')
    orderQuantityLevel = serializers.CharField(source='order_point')
    qrCode = serializers.CharField(source='id')
    quantity = serializers.CharField(source='amount')

    class Meta:
        model = Compartment
        fields = ('placement', 'storageId',
                  'qrCode', 'quantity', 'normalOrderQuantity',
                  'orderQuantityLevel', 'article')


class StorageSerializer(serializers.ModelSerializer):
    ''' compartments = storageManagemetnServisce(storage.id)'''
    class Meta:
        model = Storage
        fields = ('id', 'building', 'floor')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInfo
        fields = ('id', 'group_name')


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    userId = serializers.CharField(source='by_user.id', read_only=True)
    timeStamp = serializers.CharField(source='time_of_transaction', read_only=True)
    lioNr = serializers.PrimaryKeyRelatedField(source='article.lio_id', read_only=True)
    storageId = serializers.PrimaryKeyRelatedField(source='storage.id', read_only=True)
    quantity = serializers.IntegerField(source='amount', read_only=True)


    class Meta:
        model = Transaction
        fields = ('id', 'userId', 'timeStamp', 'lioNr',
                  'storageId', 'quantity', 'unit', 'operation')

    # def create(self, validated_data):
    #     displayed = validated_data.pop('operation')
    #     back_dict = {k:v for v, k in models.Experiment.RESULTS}
    #     res = back_dict[displayed]
    #     validated_data.update({'inferred_result': res})
    #     return super(ResultsSeializer, self).create(validated_data)

class AlternativeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlternativeArticleName
        fields = ('name',)

# class MultiStorageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Storage,Compartment
#         field


class UnitsSerializer(serializers.ModelSerializer):
    outputPerInput = serializers.IntegerField(source='output_per_input')

    class Meta:
        model = Article
        fields = ('output', 'input', 'outputPerInput')


class ArticleSupplierSerializer(serializers.ModelSerializer):
    supplierName = serializers.CharField(
        source='article_supplier.name', read_only=True)
    supplierArticleNr = serializers.CharField(
        source='supplier_article_nr', read_only=True)

    class Meta:
        model = ArticleHasSupplier
        fields = ('supplierName', 'supplierArticleNr')


class NoArticleCompartmentSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(source='amount', read_only=True)
    qrCode = serializers.CharField(source='id', read_only=True)
    normalOrderQuantity = serializers.IntegerField(
        source='standard_order_amount')
    orderQuantityLevel = serializers.IntegerField(
        source='order_point', read_only=True)
    storageId = serializers.PrimaryKeyRelatedField(
        source='storage.id', read_only=True)

    class Meta:
        model = Compartment
        fields = ('placement', 'storageId', 'qrCode', 'quantity',
                  'normalOrderQuantity', 'orderQuantityLevel')


class ApiArticleSerializer(serializers.ModelSerializer):
    lioNr = serializers.CharField(
        source='lio_id', read_only=True)
    inputUnit = serializers.CharField(
        source='input', read_only=True)
    outputUnit = serializers.CharField(
        source='output', read_only=True)
    outputPerInputUnit = serializers.IntegerField(
        source='output_per_input', read_only=True)
    alternativeNames = AlternativeNameSerializer(
        source='alternativearticlename_set', read_only=True, many=True)
    suppliers = ArticleSupplierSerializer(
        source='articlehassupplier_set', read_only=True, many=True)
    alternativeProducts = serializers.PrimaryKeyRelatedField(
        source='alternative_articles', read_only=True, many=True)
    compartments = NoArticleCompartmentSerializer(
        source='compartment_set', read_only=True, many=True
    )

    class Meta:
        model = Article
        fields = (
            'compartments', 'inputUnit', 'outputUnit',
            'outputPerInputUnit', 'price', 'suppliers', 'name',
            'alternativeNames', 'lioNr', 'alternativeProducts', 'Z41')


class OrderedArticleSerializer(serializers.ModelSerializer):
    orderedQuantity = serializers.CharField(source= 'quantity')
    articleInfo = ApiArticleSerializer(source='article', read_only=True, many=False)
    
    class Meta:
        model = OrderedArticle
        fields = ('articleInfo', 'orderedQuantity', 'unit')


class OrderSerializer(serializers.ModelSerializer):
    articles = OrderedArticleSerializer(
        source='orderedarticle_set', read_only=True, many=True)
    storageId = serializers.CharField(source='to_storage')
    orderDate = serializers.CharField(source='order_date')
    estimatedDeliveryDate = serializers.CharField(
        source='estimated_delivery_date')
    state = serializers.CharField(source='order_state')
    
    class Meta:
        model = Order
        fields = ['id', 'storageId', 'orderDate',
                  'estimatedDeliveryDate', 'state', 'articles']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('floor', 'building')


class ApiCompartmentSerializer(serializers.ModelSerializer):
    article = ApiArticleSerializer(read_only=True)
    quantity = serializers.CharField(source='amount', read_only=True)
    qrCode = serializers.CharField(source='id', read_only=True)
    normalOrderQuantity = serializers.IntegerField(
        source='standard_order_amount')
    orderQuantityLevel = serializers.IntegerField(
        source='order_point', read_only=True)
    storageId = serializers.PrimaryKeyRelatedField(
        source='storage.id', read_only=True)

    class Meta:
        model = Compartment
        fields = ('placement', 'storageId', 'qrCode', 'quantity',
                  'normalOrderQuantity', 'orderQuantityLevel', 'article')


class NearbyStoragesSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='storage.id', read_only=True)
    location = LocationSerializer(source='storage', read_only=True)
    compartment = serializers.SerializerMethodField('get_self_reference')

    class Meta:
        model = Compartment
        fields = ('id', 'location', 'compartment')

    def get_self_reference(self, object):
        return ApiCompartmentSerializer(object).data


class ArticleCompartmentProximitySerializer():
    '''Self made serializer, contains properties 
        article: Article, storage: Storage, is_valid(): Bool
        and data: [ApiCompartmentModel]'''
    def __init__(self, article: Article, storage: Storage):
        self.article = article
        self.storage = storage
        self.valid = True
        self.data = []
        same_floor = Q(storage__floor__iexact="1")
        same_building = Q(storage__building__iexact="1")

        if (storage.floor is None):
            self.valid = False
        if (storage.building is None):
            self.valid = False
        if (not self.valid):
            return

        nearest_comps = article.compartment_set.all().annotate(
            proximity_ordering=Case(
                When(same_building & same_floor, then=Value(2)),
                When(same_building & ~same_floor, then=Value(1)),
                When(same_floor & ~same_building, then=Value(0)),
                When(~same_floor & ~same_building, then=Value(-1)),
                output_field=IntegerField(),
            )
        ).order_by('-proximity_ordering')
        if (not nearest_comps):
            self.valid = False
        
        self.data = NoArticleCompartmentSerializer(
            nearest_comps, many=True, read_only=True).data

    def is_valid(self):
        return self.valid

