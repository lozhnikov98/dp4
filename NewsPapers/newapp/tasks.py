from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime

from newapp.models import Post, Category


@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000//news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=None,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task
def weekly_newsletter():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': f'http://127.0.0.1:8000/',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Публикации за неделю',
        body='',
        from_email=None,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()