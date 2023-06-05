import json
import os
import re
import sys
import statistics
import time
from datetime import datetime

import undetected_chromedriver as uc

from undetected_chromedriver import Chrome, ChromeOptions, patcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = ChromeOptions()

# Disable JavaScript execution
chrome_options.add_argument('--disable-javascript')

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

def generate_file_name(prefix = "news"):
    os.makedirs("news_detailed", exist_ok=True)
    timestamp = datetime.now().strftime("%H-%M-%S %d-%m-%Y")

    # Define the filename with the timestamp
    filename = f"./news_detailed/{prefix}_{timestamp}.txt"
    print("saving in ", filename)
    return filename


def load_data(file_path):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access the loaded data
    return (data)


def save_local(data):
    os.makedirs("news", exist_ok=True)
    timestamp = datetime.now().strftime("%H-%M-%S %d-%m-%Y")

    # Define the filename with the timestamp
    filename = f"./news_detailed/{timestamp}.json"

    # Save the list of dictionaries in JSON format
    with open(filename, "w") as file:
        json.dump(data, file)

    print(f"JSON data saved in {filename}.")


driver = Chrome(options=chrome_options, use_subprocess=True)


def find_div_with_text(url, text):
    options = ChromeOptions()
    # options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

    try:
        driver.get(url)
        page_source = driver.page_source
        data={}
        if text in page_source:
            text_xpath = f"//*[contains(text(), '{text}')]/ancestor::div"
            div_element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, text_xpath)))
            article = ""
            if div_element:
                src = driver.current_url.split('www.')[-1].split('/')[0]
                try:
                    images = div_element.find('img')['src']
                except:
                    images = []

                article = get_relatively_long_strings(div_element.text.split('\n'))

                data = {
                    "source": src if src else "",
                    "text": article,
                    "images": images
                }
            return data
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    file = sys.argv[1:]
    if file:
        data = load_data(file)
    else:
        data = load_data('news/18-51-38 03-06-2023.json')
    with open(generate_file_name(prefix="failed"), "w") as failed, open(generate_file_name(prefix="news"), "w") as news_file:
        for index,d in enumerate(data):
            try:
                print(f"********Going to next page [ {index+1} of {len(data)} ] **********")
                url = d.get('url')
                text = d.get('title')
                print(url, text)
                # extract_articles(url)
                detail = find_div_with_text(url, text)
                print(detail)
                if detail:
                    news_file.write(f"{detail}\n")
                else:
                    failed.write(f"{d}\n")
                time.sleep(2)
            except Exception as e:
                print(f"{e}")
