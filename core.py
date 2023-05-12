import datetime
import json
import os
import urllib

import requests
from bs4 import BeautifulSoup as Soup
from GoogleNews import GoogleNews

# https://pypi.org/project/GoogleNews/
googlenews = GoogleNews(lang='ar', region='EG')
print(googlenews.getVersion())
googlenews.enableException(True)

WORDS_COUNT = 150


def get_details(g, url):
    try:
        if not 'https://' in url:
            url = 'https://' + url

        response = requests.get(url)
        final_url = response.url
        domain = final_url.split('www.')[-1].split('.')[0]
        print("URL", final_url)
        req = urllib.request.Request(final_url, headers=g.headers)
        response = urllib.request.urlopen(req)
        page = response.read()
        content = Soup(page, "html.parser")

        tags = set(content.find_all())

        # extract the names of the tags
        article_tags = [tag.name for tag in tags if 'article' in tag.name]
        # print(f"Article tag : {article_tags[0]}")

        articles = content.find(article_tags[0])
        tags = articles.find_all(['p', 'h3'])
        # Extract text from each tag
        text_list = [tag.get_text() for tag in tags]  # Get the text from each <p> tag
        article_text = "\n".join(text_list)
        # article_body_div = content.find("div", {"id": "articleBody"})
        # if not article_body_div:
        #     article_body_div = content.find("div", {"id": "NewsStory"})
        # article_text = article_body_div.get_text().strip()
        img_data_src = []
        try:
            """the img tag is in article tag, and the url contains domain name"""
            imgs = articles.find_all('img')
            img_data_src = [im.get('data-src') for im in imgs if im.get('data-src') and domain in im.get('data-src')]
        except:
            print("Image not found Exception")
        if article_text:
            words = len(article_text.split(' '))
            if words < WORDS_COUNT:
                print(f"Ignoring because of less words : {words}")
                return None
        print("News load success")

        return {"img": img_data_src, "link": final_url, "detail": article_text}

    except Exception as e:
        print(f"Ignoring because of {e}")
        return None


def website_allowed(website, news):
    if not news:
        return True
    news = news.split(",")
    print(news)

    domain = website.split('www.')[-1].split('.')[0]
    for n in news:
        if domain in n:
            return True
    else:
        return False


def scrap_event(news):
    try:
        # googlenews.set_lang('ar')
        googlenews.set_period('7d')
        # googlenews.set_time_range('03/21/2023', '03/22/2023')  # mm/dd/yy
        googlenews.set_encode('utf-8')
        googlenews.search('رياضة')
        # googlenews.search('sports')

        # googlenews.get_news()
        results = googlenews.results(sort=True)
        data = []
        for result in results:
            website = result.get('link')
            print(f"Scrapint Website: {website}")
            if website_allowed(website, news):
                detail = get_details(googlenews, website)
                if detail:
                    result.update(detail)
                    data.append(result)
                    # print(result)
        current_time = datetime.datetime.now()
        timestamp = (current_time.timestamp())
        # news = googlenews.get_texts()
        # print("Done : ", news)
        googlenews.clear()
        return str(data)
    except Exception as e:
        print(f"Google News failed: {e}")


if __name__ == '__main__':
    print(scrap_event([]))
