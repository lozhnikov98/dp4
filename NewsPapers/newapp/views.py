from django.core.cache import cache
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import *
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from .filters import PostFilter
from .forms import PostForm


class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'authors_list.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = 'Post'
    template_name = 'post.html'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'Post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'Post-{self.kwargs["pk"]}', obj)
            return obj


class PostList(ListView):
    model = Post
    context_object_name = 'Posts'
    template_name = 'post_list.html'
    ordering = '-dateCreation'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
    # Переопределяем функцию получения списка товаров


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newapp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newapp.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostSearch(ListView):
    model = Post
    context_object_name = 'Posts'
    template_name = 'search.html'
    ordering = '-dateCreation'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    postCategory = Category.objects.get(id=pk)
    postCategory.subscribers.add(user)

    message = "Вы успешно подписались на рассылку публикаций категории"
    return render(request, 'subscribe.html', {'postCategory': postCategory, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    postCategory = Category.objects.get(id=pk)
    postCategory.subscribers.remove(user)

    message = "Вы успешно отписались от рассылки публикаций категории"
    return render(request, 'subscribe.html', {'postCategory': postCategory, 'message': message})