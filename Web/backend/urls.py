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
    path('transactions/addinputunit/<str:storage_space_id>/<int:amount>/',
         csrf_exempt(views.AddInputUnit.as_view())),
    path('transactions/addoutputunit/<str:storage_space_id>/<int:amount>/',
         csrf_exempt(views.AddOutputUnit.as_view())),
    path('transactions/returnunit/<str:storageSpaceId>/<int:amount>/',
         views.ReturnUnit.as_view()),
]

urlpatterns = format_suffix_patterns(urlPatterns)
