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


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


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
