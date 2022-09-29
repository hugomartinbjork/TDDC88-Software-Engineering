from rest_framework import serializers
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.coremodels.storageComponent import storageComponent

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('name', 'lioId')

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ('name',)

class StorageComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = storageComponent
        fields = ('qrId', 'article', 'storage', 'amount', 'standardOrderAmount', 'orderpoint',)