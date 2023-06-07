import json
import os
import time
from datetime import datetime

from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions

news = []
base_url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JXVnVMVWRDR2dKUVN5Z0FQAQ?hl=ar&gl=EG&ceid=EG:ar"
scroll_count = 8
delay = 5

chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
# Disable JavaScript execution
chrome_options.add_argument('--disable-javascript')
driver = Chrome(options=chrome_options, use_subprocess=True, version_main=114)


def save_local(data):
    os.makedirs("news", exist_ok=True)
    timestamp = datetime.now().strftime("%H-%M-%S %d-%m-%Y")

    # Define the filename with the timestamp
    filename = f"./news/{timestamp}.json"

    # Save the list of dictionaries in JSON format
    with open(filename, "w") as file:
        json.dump(data, file)

    print(f"JSON data saved in {filename}.")
    return filename


def load_page_content():
    driver.get(base_url)
    # Scroll down the page multiple times to load more content
    for i in range(scroll_count):
        print(f"Scroll count === {i + 1}")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)


def get_page_content():
    # Get the page content
    content = driver.page_source

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
    print("-------------------------")
    print(len(news))
    return save_local(data=news)


def main():
    print("Started...")
    load_page_content()
    file_name = get_page_content()
    print(f"Saved news data in file: {file_name}")
    driver.quit()  # Close the browser
    return file_name


if __name__ == "__main__":
    main()
