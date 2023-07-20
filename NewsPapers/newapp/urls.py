from django.urls import path
from .views import (AuthorList, PostDetail,
                    PostList, PostCreate,
                    PostUpdate, PostDelete,
                    PostSearch)


urlpatterns = [
    path('authors/', AuthorList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search')
]