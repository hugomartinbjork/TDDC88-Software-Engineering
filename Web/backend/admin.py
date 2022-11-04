from django.contrib import admin
from backend.coremodels.alternative_article_name import AlternativeArticleName
from backend.coremodels.inputOutput import InputOutput
from backend.coremodels.article import Article
from backend.coremodels.centralStorageSpace import CentralStorageSpace
from backend.coremodels.storage_unit import StorageUnit
# from backend.coremodels.storageComponent import storage_unit
from backend.coremodels.cost_center import CostCenter
from backend.coremodels.user_info import UserInfo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from backend.coremodels.article import GroupInfo
from django.contrib.auth.models import Group
from backend.coremodels.qr_code import QRCode
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.article_has_supplier import ArticleHasSupplier
from backend.coremodels.supplier import Supplier
from backend.coremodels.transaction import Transaction
from backend.coremodels.order import Order
from django.utils.html import format_html


# Register your models here.
# admin.site.register(storage_unit)
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

admin.site.register(StorageSpace)


# Displays all articles in the group
class ArticleAdminInline(admin.TabularInline):
    model = Article.article_group.through


class GroupAdmin(admin.ModelAdmin):
    inlines = (ArticleAdminInline, )


admin.site.register(GroupInfo, GroupAdmin)
#######################################################


admin.site.register(Supplier)

# Displays which storage components that the articles are in, the supplier that the article has and its alternative names
class StorageSpaceInline(admin.TabularInline):
    model = StorageSpace

class ArticleHasSupplierInline(admin.TabularInline):
    model = ArticleHasSupplier

class AlternativeNameInLine(admin.TabularInline):
    model = AlternativeArticleName

class ArticleAdmin(admin.ModelAdmin):
    inlines = (StorageSpaceInline, ArticleHasSupplierInline, AlternativeNameInLine, )


admin.site.register(Article, ArticleAdmin)
########################################################


class StorageAdmin(admin.ModelAdmin):
    inlines = (StorageSpaceInline, )


# Display QRCode in Backend
admin.site.register(QRCode)
admin.site.register(StorageUnit, StorageAdmin)

admin.site.register(Order)
admin.site.register(CentralStorageSpace)


########################################################


# Display Transaction in Backend
class TransactioInline(admin.TabularInline):
    model = Transaction


admin.site.register(Transaction)
