from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateTimeFilter
from .models import Category
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    title = CharFilter(
        lookup_expr='icontains',
        field_name='title',
        label='Заголовок',
    )

    category = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Любая',
    )
    date = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата',
        widget=DateTimeInput(
            attrs={'type': 'date'},
        ),
    )