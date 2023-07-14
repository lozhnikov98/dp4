from django.contrib import admin
from django.urls import path, include
from .views import AuthorList, PostDetail, PostList


urlpatterns = [
    path('authors/', AuthorList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('', PostList.as_view()),
]