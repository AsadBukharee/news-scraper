import datetime
import json
import os
import urllib

import requests
from bs4 import BeautifulSoup as Soup, BeautifulSoup
from GoogleNews import GoogleNews

# https://pypi.org/project/GoogleNews/
googlenews = GoogleNews(lang='ar', region='EG')
print(googlenews.getVersion())
googlenews.enableException(True)

WORDS_COUNT = 150
NEWS_SITES = [
    "filgoal.com",
    "elbalad.news",
    "skynewsarabia.com",
    "beinsports.com",
    "elaosboa.com",
    "kooora.com"
    # "goal.com"
]


def get_url(news):
    for n in NEWS_SITES:
        if news in n:
            if not 'https://' in n:
                url = 'https://' + n

            if "filgoal" in url:
                return url + "/ar"
            if "goal" in url:
                return url + "/ar"

            if "elbalad" in url:
                url = url + "/category/5"
            if "skynewsarabia" in url:
                url = url + "/sport"
            if "beinsports" in url:
                url = url + "/ar/"
            if "elaosboa" in url:
                url = url + "/category/sports/"
            return url


def get_article_urls(url):
    article_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if "goal" in url:
        article_urls = [link.get('href') for link in soup.find_all('a') if
                        link.get('href') and '/ar/%' in link.get('href') and 'goal' in link.get('href')]

    if "elaosboa" in url:
        art = soup.find_all('article')
        article_urls = [link.find('a').get('href') for link in art if link.find('a')]

    if "kooora" in url:
        art = soup.find('div', {'class': 'newsList'})
        article_urls = [link.get('href') for link in art.find_all('a') if
                        link.get('href')]

    if "beinsports" in url:
        article_urls = [link.get('href') for link in soup.find_all('a') if
                        link.get('href') and '/ar/%' in link.get('href')]

    if "filgoal" in url:
        article_urls = ["https://www.filgoal.com" + link.get('href') for link in soup.find_all('a') if
                        link.get('href') and '/articles/' in link.get('href')]

    if "elbalad" in url:
        news_list_div = soup.find('div', {'class': 'news-list'})
        article_urls = ["https://www.elbalad.news/" + a_tag['href'] for a_tag in news_list_div.find_all('a')]
    if "skynewsarabia" in url:
        article_urls = ["https://www.skynewsarabia.com" + link.get('href') for link in soup.find_all('a') if
                        link.get('href') and '/sport/' in link.get('href')]

    return article_urls


def get_details(g, url):
    try:
        # if not 'http://' in url:
        #     url = 'http://' + url

        response = requests.get(url)
        if response.status_code == 200:
            final_url = response.url
            domain = final_url.split('www.')[-1].split('.')[0]
            print("URL", final_url)
            req = urllib.request.Request(final_url, headers=g.headers)
            response = urllib.request.urlopen(req)
            page = response.read()
            content = Soup(page, "html.parser")

            tags = set(content.find_all())

            # extract the names of the tags
            # article_tags need to be tested.
            article_tags = [tag.name for tag in tags if 'article' in tag.name]
            # print(f"Article tag : {article_tags[0]}")

            if "beinsports" in url:
                articles = content.find(article_tags[0], {'class': 'homepage'})

            articles = content.find(article_tags[0])
            tags = articles.find_all(['p', 'h3'])
            # Extract text from each tag
            text_list = [tag.get_text() for tag in tags]  # Get the text from each <p> tag
            article_text = "\n".join(text_list)

            img_data_src = []
            try:
                """the img tag is in article tag, and the url contains domain name"""
                imgs = articles.find_all('img')
                if "elaosboa" in url:
                    img_data_src = [im.get('data-src') for im in imgs if
                                    im.get('data-src') and domain in im.get('data-src') and "uploads" in im.get(
                                        'data-src')]

                if "beinsports" in url:
                    img_data_src = [im.get('src') for im in imgs if
                                    im.get('src') and domain in im.get('src') and "images" in im.get('src')]
                    if not img_data_src:
                        img_data_src = [im.get('data-src') for im in imgs if
                                        im.get('data-src') and domain in im.get('data-src') and "images" in im.get(
                                            'data-src')]

                if "filgoal" in url:
                    img_data_src = [im.get('data-src') for im in imgs if
                                    im.get('data-src') and domain in im.get('data-src') and "verylarge" in im.get(
                                        'data-src')]
                if "skynewsarabia" in url:
                    img_data_src = [im.get('src') for im in imgs if
                                    im.get('src') and domain in im.get('src') and "images/" in im.get('src')]

                if "elbalad" in url:
                    img_data_src = [im.get('srcset') for im in imgs if
                                    im.get('srcset') and "UploadCache" in im.get('srcset')]
                    if img_data_src:
                        s = img_data_src[0]
                        start = s.find("/")
                        end = s.find(".jpeg", start) + 5
                        img_data_src = "https://www.elbalad.news/" + s[start:end]

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


def scrap_event():
    try:
        # googlenews.set_lang('ar')
        googlenews.set_period('7d')
        # googlenews.set_time_range('03/21/2023', '03/22/2023')  # mm/dd/yy
        googlenews.set_encode('utf-8')
        googlenews.search('رياضة')
        # googlenews.search('sports')

        # googlenews.get_news()
        results = googlenews.results(sort=False)
        data = []
        for result in results:
            website = result.get('link')
            print(f"Scrapint Website: {website}")
            # if website_allowed(website, news):
            detail = get_details(g=googlenews, url=website)
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


def scrap_custom(news):
    results = []

    for n in news:
        print(f"{'*'*40}\n Scraping {n}")
        url = get_url(n)
        if url:
            if "kooora" in url:
                results.append("Coming soon")
            # if "/goal" in url:
            #     results.append("Coming soon")
            article_urls = get_article_urls(url)
            for i, u in enumerate(article_urls):
                print(f"Enum => {i + 1} : {n} of {len(article_urls)}")
                detail = get_details(g=googlenews, url=u)
                if detail:
                    results.append({url: detail})
    return results


if __name__ == '__main__':
    print(scrap_event([]))
