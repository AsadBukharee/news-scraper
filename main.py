import asyncio
import os
import sys
from typing import List, Optional
from fastapi import FastAPI, Query, Depends, BackgroundTasks
from fastapi.responses import PlainTextResponse
from starlette.responses import RedirectResponse
from load_all_news_detail import get_detaild_news_from_latest_file, get_latest_scraped, driver
from core import scrap_event, scrap_custom, NEWS_SITES
from load_all_news_meta import main

app = FastAPI()
worker_process = None
background_tasks_ = []

def parse_list(news: Optional[List[str]] = Query(None, title="News Sites",
                                                 description=f"Select from this list of news sites  {NEWS_SITES}")) -> \
        Optional[List]:
    """
    accepts strings formatted as lists with square brackets
    names can be in the format
    "[bob,jeff,greg]" or '["bob","jeff","greg"]'
    """

    def remove_prefix(text: str, prefix: str):
        return text[text.startswith(prefix) and len(prefix):]

    def remove_postfix(text: str, postfix: str):
        if text.endswith(postfix):
            text = text[:-len(postfix)]
        return text

    if news is None:
        return

    # we already have a list, we can return
    if len(news) > 1:
        return news

    # if we don't start with a "[" and end with "]" it's just a normal entry
    flat_names = news[0]
    if not flat_names.startswith("[") and not flat_names.endswith("]"):
        return news

    flat_names = remove_prefix(flat_names, "[")
    flat_names = remove_postfix(flat_names, "]")

    names_list = flat_names.split(",")
    names_list = [remove_prefix(n.strip(), "\"") for n in names_list]
    names_list = [remove_postfix(n.strip(), "\"") for n in names_list]

    return names_list


@app.on_event('startup')
async def startup_event():
    print("News server is started")


@app.on_event("shutdown")
async def shutdown_event():
    print("News server is shutting down")

@app.get("/kill-atsks")
async def root():
    driver.close()
@app.get("/")
async def root():
    # Redirect the root URL to the API documentation
    return RedirectResponse(url="/docs")

@app.get('/word-count', description="You can set the threshold words count, by default it is 150")
def set_word_count(count: int = 200):
    global WORDS_COUNT
    WORDS_COUNT = count
    return {"message": f"word count set to {count}", "data": []}


@app.get('/news-sites', description="it provides the list of available news sites. for manual scraping")
def get_news_sites():
    global NEWS_SITES
    return {"message": f"Available news sites: {NEWS_SITES}"}


@app.get("/sources", description="enter the news sites form available news sites or enter nothing to scrap from google")
async def get_news(news: List[str] = Depends(parse_list)):
    """ list param method """
    # print(news)
    if news:
        """scrap from the given news sources"""
        results = await scrap_custom(news)
        return {"message": results}
    else:
        name = await main()
        return {
            "message": f"A background service has started and it will save the articles meta in a news directory, tas ID : {name}"}
        # return Response(scrap_event(), media_type="text/plain")


@app.get('/all-google-articles', description="Scrapes all news sports articles meta data and saves in news article,")
async def get_news_sites():
    name = main()
    # get_detaild_news_from_latest_file(file=None)
    return {"message": f"file saved in news: {name}"}


@app.post("/start-detail-task",
          description="It returns nothing, instead starts a background srvice that scraps news from meta files and saves in a directory")
async def start_task(background_tasks: BackgroundTasks):
    task = background_tasks.add_task(get_detaild_news_from_latest_file)
    background_tasks_.append(task)
    return {"message": f"Task has been started in the background.{task}"}


@app.get('/scraped-files-list', description="It returns the list of available scrapped files.")
async def scraped_files_list():
    directory = 'news_detailed/passed'
    files = os.listdir(directory)
    return {"available files": f"{files}"}


@app.get('/get-latest-scraped/{file_name}')
async def get_news_sites(file_name: str = None):
    print(f'Request received for {file_name}')
    text = get_latest_scraped(file_name=file_name)
    if text:
        return PlainTextResponse(f"{text}")
    else:
        return {"data": "error"}


if __name__ == "__main__":
    news = arguments = sys.argv[1:]  # ['elbalad','filgoal']
    print(news)
    if news:
        """scrap from the given news sources"""
        results = scrap_custom(news)
        print(results)
    else:
        print(scrap_event())
