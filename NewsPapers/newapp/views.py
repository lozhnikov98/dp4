from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
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


class PostList(ListView):
    model = Post
    context_object_name = 'Posts'
    template_name = 'post_list.html'
    ordering = '-dateCreation'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
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
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


# class PostCreate(LoginRequiredMixin, CreateView):
#     raise_exception = True
#     form_class = PostForm
#     model = Post
#     template_name = 'post_edit.html'