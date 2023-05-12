import ast
import datetime
import json
from bidi.algorithm import get_display
import requests
from bs4 import BeautifulSoup
from celery.utils.serialization import jsonify



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


# def remove_duplicates():
#     news_keys = redis_client.get('news_keys')
#     if news_keys:
#         news_keys = ast.literal_eval(news_keys.decode())
#     for key in news_keys:
#         key = 1679084429
#         news_doc = redis_client.get(f'{key}')
#         if news_doc:
#             news_doc = news_doc.decode().replace("\'",'"')
#             pt = get_display(news_doc)
#             jt = json.loads(get_display(pt))
#             print(jt.keys())
#             print(news_doc)


def get_details_news():
    from GoogleNews import GoogleNews
    import requests
    from bs4 import BeautifulSoup

    # create a GoogleNews object
    gn = GoogleNews()

    # search for articles related to sports
    gn.search('sports')

    # get the news articles
    news = gn.results()

    # get the first article URL
    article_url = news[0]['link']

    # get the HTML content of the article page


# def scrap_elaosboa():
#     try:
#         url = "https://www.elaosboa.com/"
#         response = session.get(url, headers=HEADERS)
#
#         # Parse the HTML content of the response using Beautiful Soup
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         # Find all the div elements with class "item-li"
#         items = soup.find_all('article')  # , class_='item-li')
#
#         # Create an empty list to store the tuples
#         results = []
#         i=0
#         # Loop through the items and extract the information you need
#         for item in items:
#
#             if i==2:
#                 break
#             # Extract the URL from the href attribute of the a tag
#             news_url = item.a['href']
#             details = get_details_news(news_url, tag='post-entry')
#
#             if details:
#                 i += 1
#                 data = {"news_url": news_url,
#                         "image": item.a.find('img')['src'] if item.a.find('img')['data-src'] is None else
#                         item.a.find('img')['data-src'],
#                         "title": item.a.find('img')['title'].strip(),
#                         "details": details
#                         }
#
#                 # Create a tuple of the extracted information and append it to the results list
#                 results.append(data)
#
#         # Print the list of tuples
#         # print(results)
#         current_time = datetime.datetime.now()
#         timestamp = int(current_time.timestamp())
#         value = {"scraped_at": timestamp, "website": "elaosboa", "news_list": results}
#
#         print("Done : ", timestamp)
#         return True
#     except Exception as e:
#         return str(e)
#
#



if __name__ == '__main__':
    get_details_news()
