import sys
from typing import List, Optional

from fastapi import FastAPI, Query, Depends

from cache.all_google_sports_articles import get_all_from_google
from load_all_news_detail import get_detaild_news_from_latest_file
from core import scrap_event, scrap_custom
from load_all_news_meta import main

app = FastAPI()
worker_process = None



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
def shutdown_event():
    print("News server is shutting down")


@app.get('/word-count')
def set_word_count(count: int = 200):
    global WORDS_COUNT
    WORDS_COUNT = count
    return {"message": f"word count set to {count}", "data": []}


@app.get('/news-sites')
def get_news_sites():
    global NEWS_SITES
    return {"message": f"Available news sites: {NEWS_SITES}"}


@app.get("/sources")
def get_news(news: List[str] = Depends(parse_list)):
    """ list param method """
    # print(news)
    if news:
        """scrap from the given news sources"""
        results = scrap_custom(news)
        return {"message": results}
    else:
        return {"message": scrap_event()}
        # return Response(scrap_event(), media_type="text/plain")

@app.get('/all-google-articles')
async def get_news_sites():
    name = await main()
    return {"message": f"file saved in news: {name}"}

@app.get('/start-scraping')
async def get_news_sites():
    print('Request received')
    name = await get_all_from_google()
    return {"message": f"file saved in news: {name}"}


if __name__=="__main__":
    news = arguments = sys.argv[1:]#['elbalad','filgoal']
    print(news)
    if news:
        """scrap from the given news sources"""
        results = scrap_custom(news)
        print(results)
    else:
        print(scrap_event())