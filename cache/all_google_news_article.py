import asyncio
import os

from bs4 import BeautifulSoup
import json
from datetime import datetime
from undetected_chromedriver import Chrome, ChromeOptions

news = []
base_url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=ar&gl=EG&ceid=EG:ar"
timeout = 200
scroll_count = 8
delay = 5


def save_local(data):
    os.makedirs("../news", exist_ok=True)
    timestamp = datetime.now().strftime("%H-%M-%S %d-%m-%Y")

    # Define the filename with the timestamp
    filename = f"./news/{timestamp}.json"

    # Save the list of dictionaries in JSON format
    with open(filename, "w") as file:
        json.dump(data, file)

    print(f"JSON data saved in {filename}.")
    return filename


async def extract_articles():
    print("Worker has started scraping the articles")

    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    with Chrome(options=options,version_main=114) as browser:
        tab = browser.new_tab()
        await tab.goto(base_url, options={'timeout': int(timeout * 1000)})

        # Scroll down multiple times to load more content
        for i in range(scroll_count):
            print(f"Scroll count === {i + 1}")
            await tab.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(delay=delay)

        # Extract the page content
        content = await tab.content()

        # Create BeautifulSoup object
        soup = BeautifulSoup(content, 'html.parser')

        # Find all article tags
        article_tags = soup.find_all('article')

        # Extract URL and text from each article tag
        for index, article in enumerate(article_tags):
            url = article.find('a')['href']
            url = url.replace('./articles/', 'https://news.google.com/articles/')
            data = {
                "index": index,
                "url": url,
                "title": article.find('h4').text,
                "time": article.find('time')['datetime'],
                "when": article_tags[0].find('time').text
            }
            print(data)
            news.append(data)
        await tab.close()

    print("-------------------------")
    print(len(news))
    return save_local(data=news)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(extract_articles())
