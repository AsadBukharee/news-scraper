# **Components**
1. FastApi App to serve data through APIs
2. Redis:  Works as a Queue to hold latest data and it isalso used by celery.
3. Celery: celery worker for background tasks.
4. Core: core module to do the heavy scraping tasks.
5. Subprocess: to execute celery worker as an independent process from fastapi.

# To DOs
1. keep your custom values in .env file
2. mention the time interval to tell the scraper to scrap after INTERVAL (default value is 30 minutes) minutes

### News Scraper

This is a Python application that scrapes news articles from a specified URL and stores them in a Redis database. It uses the FastAPI framework for the API and Celery for the task scheduling.

### Installation

##### Clone the repository: 
I will update soon, for now please use this code.

`git clone https://github.com/asadbukharee/news-scraper.git`

Change into the project directory: cd news-scraper
Install the required packages: pip install -r requirements.txt
Usage
Starting the API and Celery worker
Start the FastAPI server: uvicorn main:app --reload
In a new terminal window, start the Celery worker: 
you don't need to run this while using fastapi.

`celery -A scraper worker --loglevel=INFO -P eventlet`

### Endpoints

##### /add-news

This endpoint allows you to add news articles to the Redis database.

Method: POST

Request body: JSON

    json
    Copy code
    {
        "title": "Example news article",
        "description": "This is an example news article.",
        "url": "https://example.com/news/article",
        "website": "example.com"
    }

##### /get-news

This endpoint allows you to retrieve news articles from the Redis database.

Method: GET

Parameters:

latest (optional, default: true): If true, returns only the latest news articles. If false, returns all news articles.
website (optional): If specified, returns only news articles from the specified website.
/scrape-news
This endpoint starts a Celery task to scrape news articles from a specified URL.

Method: GET

Parameters:

url (optional, default: https://www.filgoal.com/articles/): The URL of the news website to scrape.
min_word_count (optional, default: 200): The minimum word count for an article to be returned.
/send-email
This endpoint starts a Celery task to send an email containing the latest news articles.

Method: GET

Celery setup
This project uses Celery to schedule tasks. The celery_app.conf.beat_schedule dictionary in the scraper.py file contains the schedule for the tasks. You can modify this schedule to suit your needs.