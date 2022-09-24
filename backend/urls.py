from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from backend.views import views

urlPatterns = [
    path('article/<str:articleId>/', views.article.as_view()),
]

urlpatterns = format_suffix_patterns(urlPatterns)