from django.contrib import admin
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.coremodels.storageComponent import storageUnit
from backend.coremodels.article import Group

# Register your models here.
admin.site.register(Article)
admin.site.register(Storage)
admin.site.register(storageUnit)
admin.site.register(Group)


