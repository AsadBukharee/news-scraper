import ast
import datetime
import json
from bidi.algorithm import get_display
import requests
from bs4 import BeautifulSoup
from celery.utils.serialization import jsonify

from main import redis_client

WORDS_COUNT = 200
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ur;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",

}
session = requests.Session()


def remove_duplicates():
    news_keys = redis_client.get('news_keys')
    if news_keys:
        news_keys = ast.literal_eval(news_keys.decode())
    for key in news_keys:
        key = 1679084429
        news_doc = redis_client.get(f'{key}')
        if news_doc:
            news_doc = news_doc.decode().replace("\'",'"')
            pt = get_display(news_doc)
            jt = json.loads(get_display(pt))
            print(jt.keys())
            print(news_doc)


def get_details_news(url, tag):
    response = session.get(url, headers=HEADERS)

    # Parse the HTML content of the response using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    post_div = soup.find("div", class_="post-entry")  # Find the <div> with class "post-entry"

    p_tags = post_div.find_all("p")  # Find all <p> tags inside the <div>

    text_list = [p.text for p in p_tags]  # Get the text from each <p> tag

    text = "\n".join(text_list)
    if len(text.split(' ')) < WORDS_COUNT:
        print('Ignored')
        return None
    print('Retained')
    return text


def store_redis(timestamp, value):
    try:
        expiry_seconds = 48 * 60 * 60
        news_keys = redis_client.get('news_keys')
        if news_keys:
            news_keys = ast.literal_eval(news_keys.decode())
            news_keys.append(timestamp)
        else:
            news_keys = [timestamp]
        redis_client.setex('news_keys', value=f"{news_keys}", time=expiry_seconds)
        redis_client.setex(f"{timestamp}", value=f"{value}", time=expiry_seconds)
        return True
    except:
        return False


def scrap_elaosboa():
    try:
        url = "https://www.elaosboa.com/"
        response = session.get(url, headers=HEADERS)

        # Parse the HTML content of the response using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the div elements with class "item-li"
        items = soup.find_all('article')  # , class_='item-li')

        # Create an empty list to store the tuples
        results = []
        i=0
        # Loop through the items and extract the information you need
        for item in items:

            if i==2:
                break
            # Extract the URL from the href attribute of the a tag
            news_url = item.a['href']
            details = get_details_news(news_url, tag='post-entry')

            if details:
                i += 1
                data = {"news_url": news_url,
                        "image": item.a.find('img')['src'] if item.a.find('img')['data-src'] is None else
                        item.a.find('img')['data-src'],
                        "title": item.a.find('img')['title'].strip(),
                        "details": details
                        }

                # Create a tuple of the extracted information and append it to the results list
                results.append(data)

        # Print the list of tuples
        # print(results)
        current_time = datetime.datetime.now()
        timestamp = int(current_time.timestamp())
        value = {"scraped_at": timestamp, "website": "elaosboa", "news_list": results}
        store_redis(timestamp=timestamp, value=value)
        print("Done : ", timestamp)
        return True
    except Exception as e:
        return str(e)


def scrape_elbalad(min_word_count=200):
    url = 'https://www.elbalad.news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = []
    image_urls = []

    print("===================================================")
    print("                Scrap Task Started                 ")
    print("===================================================")
    lis = soup.find_all("li")
    for ind, article in enumerate(lis):
        print(f"News Count : {ind}")
        for li in lis:
            a = li.find("a")
            href = a.get("href")
            title = a.find("h6").text.strip()
            print(a, href, title)
        # text = article.text.strip()
        # words = text.split()
        # if len(words) >= min_word_count:
        #     paragraphs.append(text)
        #     image = article.find('img')
        #     if image is not None and 'src' in image.attrs:
        #         image_urls.append(image['src'])

    print("===================================================")
    print("                Scrap Task Finished                 ")
    print("===================================================")
    return paragraphs, image_urls


if __name__ == '__main__':
    # scrap_elaosboa()
    remove_duplicates()
