from rest_framework import serializers

from backend.coremodels.alternative_article_name import AlternativeArticleName
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
        fields = ('name', 'lio_id', 'description',
                  'article_group', 'image', 'Z41', 'price',
                  'alternative_articles')


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('name',)


class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('id', 'name', 'users')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('user', 'cost_center')


class CompartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compartment
        fields = ('id', 'storage', 'article',
                  'order_point', 'standard_order_amount',
                  'maximal_capacity', 'amount')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInfo
        fields = ('id', 'group_name')


class OrderedArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedArticle
        fields = ('article')


class OrderSerializer(serializers.ModelSerializer):
    article = OrderedArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'to_storage', 'order_date',
                  'estimated_delivery_date', 'order_state', 'article']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'storage', 'by_user', 'article',
                  'amount', 'time_of_transaction', 'operation')


class AlternativeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlternativeArticleName
        fields = ('name',)


class UpdateInputOutoutSerializer(serializers.ModelSerializer):

    input = serializers.CharField(source="input_unit_name")
    output = serializers.CharField(source="output_unit_name")
    outputPerInput = serializers.IntegerField(source="output_unit_per_input_unit")

    class Meta:
        model = InputOutput
        fields = ('input', 'output', 'outputPerInput',)


class UpdateArticleSerializer(serializers.ModelSerializer):
    input_output = UpdateInputOutoutSerializer()
    #units = serializers.CharField(source="input_output")

    class Meta:
        model = Article
        fields = ('input_output', 'price', 'name', 'lio_id', 'alternative_articles', 'Z41',)


#Class for serializing data in ArticleToCompartmentByQRcode view
class UpdateCompartmentSerializer(serializers.ModelSerializer):
    #article = UpdateArticleSerializer()

    storageId = serializers.CharField(source="storage")
    qrCode = serializers.CharField(source="id")
    quantity = serializers.IntegerField(source="amount")
    normalOrderQuantity = serializers.IntegerField(source="standard_order_amount")
    orderQuantityLevel = serializers.IntegerField(source="order_point")

    class Meta:
        model = Compartment
        fields = ('placement', 'storageId', 'qrCode', 'quantity', 'normalOrderQuantity', 'orderQuantityLevel', 'article')