from rest_framework import serializers
from backend.models import Article, Storage, storageUnit

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