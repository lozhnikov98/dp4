from django.views.decorators.cache import cache_page
from django.urls import path
from .views import (AuthorList, PostDetail,
                    PostList, PostCreate,
                    PostUpdate, PostDelete,
                    PostSearch, CategoryListView,
                    subscribe, unsubscribe)


urlpatterns = [
    path('authors/', AuthorList.as_view(), name='authors'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe')
]