from django.contrib import admin
from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
# from backend.coremodels.storageComponent import storageUnit
from backend.coremodels.cost_center import CostCenter
from backend.coremodels.user_info import UserInfo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from backend.coremodels.article import GroupInfo
from django.contrib.auth.models import Group
from backend.coremodels.storageComponent import storageComponent

# Register your models here.
# admin.site.register(storageUnit)
admin.site.register(CostCenter)


# Displays cost center as an option in the user class
class UserInfoInLine(admin.StackedInline):
    model = UserInfo

class UserGroupInLine(admin.StackedInline):
        model = Group



class UserAdmin(BaseUserAdmin):
    inlines = (UserInfoInLine, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#######################################################

# Register your models here.
# admin.site.register(Article)

admin.site.register(storageComponent)


# Displays all articles in the group
class ArticleAdminInline(admin.TabularInline):
    model = Article.article_group.through


class GroupAdmin(admin.ModelAdmin):
    inlines = (ArticleAdminInline, )


admin.site.register(GroupInfo, GroupAdmin)
#######################################################


# Displays which storage components that the articles are in
class StorageComponentInline(admin.TabularInline):
    model = storageComponent


class ArticleAdmin(admin.ModelAdmin):
    inlines = (StorageComponentInline, )


admin.site.register(Article, ArticleAdmin)
########################################################


class StorageAdmin(admin.ModelAdmin):
    inlines = (StorageComponentInline, )


admin.site.register(Storage, StorageAdmin)
