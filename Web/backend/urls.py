from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from backend.views import views
from django.views.decorators.csrf import csrf_exempt

urlPatterns = [
    path('article/<str:articleId>/', views.article.as_view()),
    path('group/<str:groupId>/', views.group.as_view()),
    path('storage/<int:storageId>/', views.storage.as_view()),
    path('storagespace/<int:storageSpaceId>/', views.storageSpace.as_view()),
    path('order/<int:id>/', csrf_exempt(views.order.as_view())),
    path('login/', views.Login.as_view()),
    path('loginwithid/', views.LoginWithId.as_view()),
    path('storages/', views.seeAllStorageUnits.as_view()),
    path('user/<int:user_id>/transactions/', views.GetUserTransactions.as_view()),
    path('storage/<str:storageId>/value', views.getStorageValue.as_view()),
    path('alternativearticles/<str:articleId>/', views.getArticleAlternatives.as_view()), #alternative articles if storage is not sent as input
    path('alternativearticles/<str:articleId>/<str:storageId>/', views.getArticleAlternatives.as_view()), #alternative articles if a storage is sent as input
]

urlpatterns = format_suffix_patterns(urlPatterns)
