from dataclasses import field
from unittest import mock
from rest_framework import serializers
from django.db.models import Q, Case, When, Value, IntegerField

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


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('id', 'name', 'users')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('user', 'cost_center')


class CompartmentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(many=False, read_only=True)

    class Meta:
        model = Compartment
        fields = ('id', 'storage', 'article',
                  'order_point', 'standard_order_amount',
                  'maximal_capacity', 'amount', 'placement')


class StorageSerializer(serializers.ModelSerializer):
    ''' compartments = storageManagemetnServisce(storage.id)'''
    class Meta:
        model = Storage
        fields = ('id', 'building', 'floor')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInfo
        fields = ('id', 'group_name')


class OrderedArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedArticle
        fields = ('quantity', 'unit')


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'to_storage', 'order_date',
                  'estimated_delivery_date', 'order_state']

    def create(self, validated_data):
        ordered_articles_data = validated_data.pop('article')
        order = Order.objects.create(**validated_data)
        for ordered_article in ordered_articles_data:
            OrderedArticle.objects.create(order=order, **ordered_article)
        return order


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'storage', 'by_user', 'article',
                  'amount', 'time_of_transaction', 'operation')


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

    def get_units(self, object):
        return UnitsSerializer(object).data


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
        fields = ('article', 'quantity', 'qrCode', 'normalOrderQuantity',
                  'orderQuantityLevel', 'storageId', 'placement')


class ApiSmallCompartmentSerializer(serializers.ModelSerializer):
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
        fields = ('quantity', 'qrCode', 'normalOrderQuantity',
                  'orderQuantityLevel', 'storageId', 'placement')


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
        
        self.data = ApiSmallCompartmentSerializer(
            nearest_comps, many=True, read_only=True).data

    def is_valid(self):
        return self.valid
