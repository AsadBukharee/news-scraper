import asyncio
import os
import time

from pyppeteer import launch
from bs4 import BeautifulSoup
import json
from datetime import datetime

news = []
timeout = 200
scroll_count = 1
delay = 2
import re


def save_local(data):
    os.makedirs("news", exist_ok=True)
    timestamp = datetime.now().strftime("%H-%M-%S %d-%m-%Y")

    # Define the filename with the timestamp
    filename = f"./news_detailed/{timestamp}.json"

    # Save the list of dictionaries in JSON format
    with open(filename, "w") as file:
        json.dump(data, file)

    print(f"JSON data saved in {filename}.")
def remove_special_characters(string):
    pattern = r'[^\w\s\u0600-\u06FF\u0750-\u077F]'  # Matches any character that is not Arabic, alphanumeric, or whitespace
    cleaned_string = re.sub(pattern, '', string)
    return cleaned_string
def is_arabic_text(string):
    string = remove_special_characters(string)
    arabic_range1 = range(0x0600, 0x06FF + 1)  # Arabic range 1
    arabic_range2 = range(0x0750, 0x077F + 1)  # Arabic range 2

    for char in string:
        char_code = ord(char)
        if (
            char_code not in arabic_range1
            and char_code not in arabic_range2
            and not char.isspace()
            and not char.isdigit()
        ):
            return False

    return True
def load_data(file_path):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access the loaded data
    return (data)

import statistics

def get_relatively_long_strings(string_list, threshold_factor=1.1):
    # Calculate mean and standard deviation of string lengths
    lengths = [len(s) for s in string_list]
    mean = statistics.mean(lengths)
    std_dev = statistics.stdev(lengths)

    # Define threshold based on standard deviation and factor
    threshold = mean + threshold_factor * std_dev

    # Filter strings above the threshold
    relatively_long_strings = [s for s in string_list if len(s) > threshold if is_arabic_text(s)]

    return relatively_long_strings

def get_top_three_longest_strings(string_list,count):
    sorted_strings = sorted(string_list, key=len, reverse=True)
    return sorted_strings[:count]
async def extract_articles(base_url,text):
    try:
        detail = {}
        browser = await launch(
            headless=False,
            defaultArgs=['--enable-features=NetworkService', '--disable-web-security']
        )
        page = await browser.newPage()
        await page.goto(base_url, options={'timeout': int(timeout * 1000)})



        # # Scroll down multiple times to load more content
        # for i in range(scroll_count):
        #     print(f"Scrol count === {i + 1}")
        #     await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        #     await asyncio.sleep(delay=delay)

        # # Extract the page content
        html_content = await page.content()
        page.close()
        # # Extract the text from the HTML content
        # page_text = await page.evaluate('(function() { return document.body.textContent; })()')
        # print(page_text)
        #Create BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all article tags
        article_tags = soup.find_all('div')
        asyncio.sleep(5)
        # Extract URL and text from each article tag
        found_divs = []
        for index, article in enumerate(article_tags):
            if text in article.text:
                # print("-----------------------------------------")
                # print(article.text)
                # print(f"Found {index}")
                # print("-----------------------------------------")
                found_divs.append(article)
        if found_divs:
            target = found_divs[-1]
            images = target.find('img')['src']
            relatively_long_strings = get_relatively_long_strings(target.text.split('\n'))

            print("*"*40)
            print(relatively_long_strings)
            print(images)
            print("*" * 40)

            detail["text"] = '\n'.join(relatively_long_strings)
            detail["image"]= images



        return detail
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    data = load_data('news/18-51-38 03-06-2023.json')
    news = []
    for d in data:
        try:
            print("********Going to next page**********")
            url = d.get('url')
            text = d.get('title')
            print(url, text)
            # extract_articles(url)
            detail = asyncio.get_event_loop().run_until_complete(extract_articles(url,text))

            if detail:
                news.append(detail)
            time.sleep(10)
        except Exception as e:
            print(f"{e}")

    save_local(data=news)