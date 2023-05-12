import subprocess
from typing import List, Optional

from fastapi import FastAPI,Response


from core import scrap_event

app = FastAPI()
worker_process = None


@app.on_event('startup')
async def startup_event():
    print("News server is started")


@app.on_event("shutdown")
def shutdown_event():
    print("News server is shutting down")


@app.get('/word_count')
def get_news(count: int = 200):
    global WORDS_COUNT
    WORDS_COUNT = count
    return {"message": f"word count set to {count}", "data": []}


@app.get("/sources")
def get_news(news: Optional[str] = None):
    return Response(scrap_event(news), media_type="text/plain")