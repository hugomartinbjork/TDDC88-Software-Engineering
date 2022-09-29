from django.contrib import admin
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.coremodels.article import Group
from backend.coremodels.storageComponent import storageComponent

# Register your models here.
admin.site.register(Article)
admin.site.register(Storage)
admin.site.register(storageComponent)

class ArticleAdminInline(admin.TabularInline):
    model = Article.article_group.through

class GroupAdmin(admin.ModelAdmin):
    inlines = (ArticleAdminInline, )
admin.site.register(Group, GroupAdmin)


