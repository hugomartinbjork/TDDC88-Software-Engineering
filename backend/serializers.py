from rest_framework import serializers
from backend.coremodels.article import Article
from backend.coremodels.article import Group
from backend.coremodels.storage import Storage
from backend.coremodels.storageComponent import storageUnit


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('name', 'lioId', 'article_group', 'image', 'description', 'std_cost', 'minimal_order_qt', 'price', 'refill_unit', 'take_out_unit', 'alternative_names',
         'alternative_articles', 'supplier', 'sup_ordernr')

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('name',)

class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = storageUnit
        fields = ('currentStock', 'article', 'storage',)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'group_name')