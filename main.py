import subprocess
from typing import List, Optional, Annotated, Union

from fastapi import FastAPI, Response, Query, Depends
from starlette.responses import StreamingResponse

from core import scrap_event, scrap_custom,NEWS_SITES

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
    print(news)
    if news:
        """scrap from the given news sources"""
        results = scrap_custom(news)
        return {"message": results}
    else:

        return Response(scrap_event(), media_type="text/plain")
