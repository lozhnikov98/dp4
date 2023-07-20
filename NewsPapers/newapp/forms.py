from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'categoryType',
            'title',
            'text',
            'postCategory',
        ]
        labels = {
            'author': 'Автор',
            'categoryType': 'Категория',
            'title': 'Заголовок',
            'text': 'Текст',
            'postCategory': 'Тема'
                }


