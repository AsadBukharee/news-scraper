import datetime
import os
from core import scrap_event
from celery import Celery
from celery.schedules import crontab
INTERVAL = 30 if (os.environ.get('INTERVAL')) is None else int((os.environ.get('INTERVAL')))
REDIS_HOST = str(os.environ.get('REDIS_HOST'))
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
app = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

@app.task
def news_task():

    print("===================================================")
    print(f"     Task Started: {datetime.datetime.now().strftime('%I:%M:%S %p %d %b, %Y')} ")
    print("===================================================")
    scrap_event()
    print("===================================================")
    print(f"     Task Ended: {datetime.datetime.now().strftime('%I:%M:%S %p %d %b, %Y')} ")
    print("===================================================")

# Schedule the task to run every 5 minutes

app.conf.beat_schedule = {
    'run-every-5-minutes': {
        'task': 'tasks.my_task',
        'schedule': crontab(minute='*/1'),
        # 'schedule': crontab(hour=17, minute=30, day_of_week='1-5'),
        # 'schedule': timedelta(seconds=10),
    },
}

if __name__ == '__main__':
    app.start()