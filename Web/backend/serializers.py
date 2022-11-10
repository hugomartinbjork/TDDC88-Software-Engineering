from backend.coremodels.alternative_article_name import AlternativeArticleName
from backend.coremodels.cost_center import CostCenter
from rest_framework import serializers
from backend.coremodels.article import Article
from backend.coremodels.article import GroupInfo
from backend.coremodels.qr_code import QRCode
from backend.coremodels.storage import Storage
# from backend.coremodels.storageComponent import storage
from backend.coremodels.cost_center import CostCenter
from backend.coremodels.user_info import UserInfo
from backend.coremodels.compartment import Compartment
from backend.coremodels.qr_code import QRCode
from backend.coremodels.order import Order
from backend.coremodels.transaction import Transaction


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


# class StorageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = storage
#         fields = ('currentStock', 'article', 'storage',)

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


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ('id', 'compartment')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'of_article', 'to_storage',
                  'expected_wait', 'order_time')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'storage', 'by_user', 'article',
                  'amount', 'time_of_transaction', 'operation')


class AlternativeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlternativeArticleName
        fields = ('name',)


class UpdateCompartmentSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = Compartment
        fields = ('storage', 'id', 'amount', 'standard_order_amount', 'order_point','article')