from django.contrib import admin
from backend.models import Article, Storage, storageUnit

# Register your models here.
admin.site.register(Article)
admin.site.register(Storage)
admin.site.register(storageUnit)
