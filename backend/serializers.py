from backend.coremodels.cost_center import CostCenter
from rest_framework import serializers
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.coremodels.storageComponent import storageUnit
from backend.coremodels.cost_center import CostCenter

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('name', 'lioId')


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('name',)


class StorageUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = storageUnit
        fields = ('currentStock', 'article', 'storage',)

class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = ('id', 'name', 'users')