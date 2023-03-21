from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

@app.task
def my_task():
    print("===================================================")
    print("                   Task Started                    ")
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
