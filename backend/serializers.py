from backend.coremodels.cost_center import CostCenter
from rest_framework import serializers
from backend.coremodels.article import Article
from backend.coremodels.article import GroupInfo

from backend.coremodels.storage_unit import StorageUnit
# from backend.coremodels.storageComponent import storageUnit
from backend.coremodels.cost_center import CostCenter
from backend.coremodels.user_info import UserInfo
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.qr_code import QRCode
from backend.coremodels.order import Order


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('name', 'lioId', 'description', 'article_group', 'image', 'sanitation_level', 'price', 'alternative_names',
                  'alternative_articles')

        


class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageUnit
        fields = ('name',)


# class StorageUnitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = storageUnit
#         fields = ('currentStock', 'article', 'storage',)

class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('id', 'name', 'users')


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('user', 'cost_center')


class StorageSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSpace
        fields = ('id', 'storage_unit', 'article', 'orderpoint', 'standard_order_amount',
                  'maximal_capacity', 'amount')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInfo
        fields = ('id', 'group_name')


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ('id', 'storage_space')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'ofArticle', 'toStorageUnit', 'expectedWait', 'orderTime')
