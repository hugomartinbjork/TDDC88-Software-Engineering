from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from backend.views import views
from django.views.decorators.csrf import csrf_exempt

urlPatterns = [
    path('articles/lio/<str:article_id>/', views.Article.as_view()),
    path('group/<str:groupId>/', views.Group.as_view()),
    path('storage/<int:storage_id>/', views.Storage.as_view()),
    path('compartment/<int:compartment_id>/', views.Compartment.as_view()),
    path('order/<int:id>/', csrf_exempt(views.Order.as_view())),
    path('login/', views.Login.as_view()),
    path('loginwithid/', views.LoginWithId.as_view()),
    path('storages/', views.SeeAllStorages.as_view()),
    path('user/<int:user_id>/transactions/',
         views.GetUserTransactions.as_view()),
    path('transactions/addinputunit/<str:compartment_id>/<int:amount>/',
         csrf_exempt(views.AddInputUnit.as_view())),
    path('transactions/addoutputunit/<str:compartment_id>/<int:amount>/',
         csrf_exempt(views.AddInputUnit.as_view())),
    path('transactions/returnunit/<str:compartment_id>/<int:amount>/',
         views.ReturnUnit.as_view()),
    path('storage/<str:storage_id>/value', views.GetStorageValue.as_view()),
    # alternative articles if storage is not sent as input
    path('alternativearticles/<str:article_id>/',
         views.GetArticleAlternatives.as_view()),
    # alternative articles if a storage is sent as input
    path('alternativearticles/<str:article_id>/<str:storage_id>/',
         views.GetArticleAlternatives.as_view()),
    path('storage/<str:storage_id>/cost', views.GetStorageCost.as_view()),
    path('searcharticles/<str:search_string>/<str:input_storage>/',
         views.SearchForArticleInStorages.as_view()),
    path('compartments/', views.Compartment.as_view()),
    path('compartments/<str:qr_code>', views.Compartment.as_view()),
    path('transactions/', views.Transactions.as_view()),
    path('transactions/<transaction_id>', views.TransactionsById.as_view()),
    # alternative urls for transactions if date is input
]

urlpatterns = format_suffix_patterns(urlPatterns)
