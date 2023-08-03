import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPapers.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_every_week': {
        'task': 'newapp.tasks.weekly_newsletter',
        'schedule': crontab(hour=8, minute=00, day_of_week=1),
    },
}

#