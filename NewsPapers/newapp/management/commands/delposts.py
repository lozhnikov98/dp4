from django.core.management.base import BaseCommand, CommandError
from newapp.models import Post


class Command(BaseCommand):
    help = 'Удаляем все посты'

    def handle(self, *args, **options):
        for 