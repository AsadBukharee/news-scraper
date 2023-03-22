import ast
import datetime
import json
import os
import urllib

import requests
from bs4 import BeautifulSoup as Soup, ResultSet

from GoogleNews import GoogleNews

# https://pypi.org/project/GoogleNews/
googlenews = GoogleNews(lang='ar', region='EG')
# googlenews = GoogleNews(lang='en', region='US')
print(googlenews.getVersion())
googlenews.enableException(True)
# googlenews = GoogleNews(period='7d')
# googlenews = GoogleNews(start='02/01/2020',end='02/28/2020')

from redis.client import Redis
import dotenv

dotenv.load_dotenv('.env')
# now we load our environment variables.
WORDS_COUNT = 150 if os.environ.get('WORDS_COUNT') is None else int(os.environ.get('WORDS_COUNT'))
LIMIT = -1 if os.environ.get('LIMIT') is None else int(os.environ.get('LIMIT'))
REDIS_HOST = str(os.environ.get('REDIS_HOST'))
REDIS_PORT = int(os.environ.get('REDIS_PORT'))
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def store_local(directory, data,titles):
    try:
        directory = f'news_jsons/{directory}/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = os.path.join(directory, 'data.json')
        with open(path, 'w') as file:
            json.dump(data, file)
        path = os.path.join(directory, 'titles.json')
        with open(path, 'w') as file:
            json.dump(titles, file)
            print('Json Export Success')
        return True
    except Exception as e:
        print(f"{e}")
        return False


def store_redis(timestamp, data, titles):
    try:
        expiry_seconds = 48 * 60 * 60
        news_keys = redis_client.get('news_keys')
        if news_keys:
            news_keys = ast.literal_eval(news_keys.decode())
            news_keys.append(timestamp)
        else:
            news_keys = [timestamp]
        if store_local(directory=f"{timestamp}",data=data,titles=titles):
            redis_client.setex('news_keys', value=f"{news_keys}", time=expiry_seconds)
        # redis_client.setex(f"{timestamp}", value=f"{value}".encode('utf-8'), time=expiry_seconds)
        return True
    except:
        return False


def get_details(g, url):
    try:
        if not 'https://' in url:
            url = 'https://' + url

        response = requests.get(url)
        final_url = response.url
        print("URL",final_url)
        req = urllib.request.Request(final_url, headers=g.headers)
        response = urllib.request.urlopen(req)
        page = response.read()
        content = Soup(page, "html.parser")
        articles = content.find('article')
        # tags = articles.find_all(['p', 'h3'])
        # # Extract text from each tag
        # text_list = [tag.get_text() for tag in tags]  # Get the text from each <p> tag
        # paragraph = "\n".join(text_list)
        article_body_div = content.find("div", {"id": "articleBody"})
        if not article_body_div:
            article_body_div = content.find("div", {"id": "NewsStory"})
        article_text = article_body_div.get_text().strip()
        imgs = articles.find('div', {'class': 'img-cont'})
        img_tag = imgs.find('img')
        data_src = img_tag['data-src']
        if article_text:
            words = len(article_text.split(' '))
            if words < WORDS_COUNT:
                print(f"Ignoring because of less words : {words}")
                return None
        return {"img": data_src, "link": final_url, "detail": article_text}

    except Exception as e:
        print(f"Ignoring because of {e}")
        return None
def scrap_event():
    # googlenews.set_lang('ar')
    googlenews.set_period('2d')
    googlenews.set_time_range('03/21/2023', '03/22/2023')  # mm/dd/yy
    googlenews.set_encode('utf-8')
    googlenews.get_news()
    results = googlenews.results(sort=False)
    data = []
    for result in results:
        detail = get_details(googlenews, result.get('link'))
        if detail:
            result.update(detail)
            data.append(result)

    current_time = datetime.datetime.now()
    timestamp = (current_time.timestamp())
    store_redis(timestamp=timestamp, data=data, titles=googlenews.get_texts())
    print("Done : ", timestamp)
    googlenews.clear()


if __name__ == '__main__':
    scrap_event()