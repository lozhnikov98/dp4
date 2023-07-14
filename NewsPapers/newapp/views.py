from datetime import datetime
from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView


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

