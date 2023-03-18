import subprocess
from fastapi import FastAPI

from controller import get_news_redis
from models import News
from scraper import celery_, scrape_news_task, email_sender
app = FastAPI()
worker_process = None

@app.on_event('startup')
async def startup_event():
    global worker_process  # Use the global variable
    print("App is started")
    cmd = 'celery -A scraper worker --loglevel=INFO -P eventlet'
    worker_process = subprocess.Popen(cmd, shell=True)
    print("Celery worker is started")

@app.on_event("shutdown")
def shutdown_event():
    global worker_process  # Use the global variable
    print("shutting down")
    worker_process.terminate()


def check_worker_status(worker_name):
    with celery_.connection() as conn:
        try:
            worker = celery_.control.inspect().ping([])
            if worker:
                return 'Active'
            else:
                return 'Idle'
        except TimeoutError:
            return 'Unreachable'

# here are our worker endpoints

@app.post("/stop-scraper")
async def get_body(data: News):
    worker_process.terminate()
    return {'status':'true','message':'worker stopped'}

@app.get('/worker-status')
def worker_status():
    status = check_worker_status('scraper')
    return {'status': status, 'message': 'worker status'}


# here are utility endpoints

@app.post("/add-news")
async def get_body(data: News):
    return data

@app.get('/scrape-news')
def scrape_news_endpoint(url: str='https://www.filgoal.com/articles/', min_word_count: int=200):
    task = scrape_news_task.delay(url, min_word_count)
    return {'task_id': task.task_id}\

@app.get('/send-email')
def send_email():
    task = email_sender.delay()
    return {'task_id': task.task_id}


@app.get('/get-news')
def get_news(lates:bool=True,website='elaosboa'):
    return get_news_redis(lates,website)


# # Celery setup
# celery_app = Celery('scraper', broker='redis://localhost:6379/0')
# celery_app.conf.timezone = 'UTC'
# celery_app.conf.beat_schedule = {
#     'scrape-every-30-minutes': {
#         'task': 'scraper.scrape_news_task',
#         'schedule': crontab(minute='*/30'),
#         'args': ('https://news.google.com', 200),
#     },
# }

# def scrape_news(url, min_word_count=200):
#     """
#     Scrapes news articles from the given URL and returns the paragraphs and image URLs.
#
#     Parameters:
#         url (str): The URL of the news website to scrape.
#         min_word_count (int): The minimum word count for an article to be returned.
#
#     Returns:
#         A tuple containing the scraped paragraphs and image URLs.
#     """
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     paragraphs = []
#     image_urls = []
#
#     for article in soup.find_all('article'):
#         text = article.text.strip()
#         words = text.split()
#         if len(words) >= min_word_count:
#             paragraphs.append(text)
#             image = article.find('img')
#             if image is not None and 'src' in image.attrs:
#                 image_urls.append(image['src'])
#
#     return paragraphs, image_urls
