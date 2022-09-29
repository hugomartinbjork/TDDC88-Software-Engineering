from django.contrib import admin
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.coremodels.article import Group
from backend.coremodels.storageComponent import storageComponent

# Register your models here.
#admin.site.register(Article)

admin.site.register(storageComponent)



#Displays all articles in the group
class ArticleAdminInline(admin.TabularInline):
    model = Article.article_group.through

class GroupAdmin(admin.ModelAdmin):
    inlines = (ArticleAdminInline, )
admin.site.register(Group, GroupAdmin)
#######################################################


#Displays which storage components that the articles are in
class StorageComponentInline(admin.TabularInline):
    model = storageComponent

class ArticleAdmin(admin.ModelAdmin):
    inlines = (StorageComponentInline, )

admin.site.register(Article, ArticleAdmin)
########################################################

class StorageAdmin(admin.ModelAdmin):
    inlines = (StorageComponentInline, )
admin.site.register(Storage, StorageAdmin)


