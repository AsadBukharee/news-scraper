import os
import requests
from bs4 import BeautifulSoup
from celery import Celery
from celery.schedules import crontab
from core import scrap_elaosboa
INTERVAL = 30 if (os.environ.get('INTERVAL')) is None else int((os.environ.get('INTERVAL')))
REDIS_HOST = str(os.environ.get('REDIS_HOST'))
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
"""prefork worker doesn't work in windows , so we have to use (-P solo) or (-P eventlet)\
as following:
celery -A scraper worker --loglevel=INFO -P eventlet
"""

celery_ = Celery('scraper',
                 broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
                 backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
                 )
# celery_.conf.beat_schedule = {
#     'scrape-every-30-minutes': {
#         'task': 'scraper.scrape_news_task',
#         'schedule': crontab(minute=f'*/{INTERVAL}'),
#         'args': ('https://news.google.com', 200),
#     },
# }
celery_.conf.beat_schedule = {
    'scrape-every-30-minutes': {
        'task': 'scraper.email_sender',
        'schedule': crontab(minute=f'*/{INTERVAL}'),
        'args': ('https://news.google.com', 200),
    },
}
celery_.conf.timezone = 'UTC'


def scrape_news():

    print("===================================================")
    print("                Scrap Task Started                 ")
    print("===================================================")
    scrap_elaosboa()
    print("===================================================")
    print("                Scrap Task Finished                 ")
    print("===================================================")
    return True


def send_email():
    try:
        print("===================================================")
        print("                Email Task Started                 ")
        print("===================================================")
    except:
        print("error")


@celery_.task
def scrape_news_task(*args):
    scrape_news()
    return {'status': 'true', 'message': 'scraper started'}


@celery_.task(name="email_sender")
def email_sender(*args):
    return send_email()
