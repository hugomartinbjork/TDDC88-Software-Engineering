from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from backend.views import views

urlPatterns = [
    path('article/<str:articleId>/', views.article.as_view()),
    path('login/', views.Login.as_view()),
    path('loginwithid/', views.LoginWithId.as_view()),
    # path('login/<str:userId>/', views.login_user_with_id.as_view()),
    # path('login/<str:username>/<str:password>', views.login_user.as_view()),
]

urlpatterns = format_suffix_patterns(urlPatterns)
