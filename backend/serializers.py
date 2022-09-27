from rest_framework import serializers
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.coremodels.storageComponent import storageUnit

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('name', 'lioId', 'image', 'description', 'price', 'refill_unit', 'take_out_unit', 'alternative_names', 'alternative_articles', 'supplier', 'sup_ordernr')

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('name',)

class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = storageUnit
        fields = ('currentStock', 'article', 'storage',)