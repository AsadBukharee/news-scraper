import json
import os
import re
import statistics
import sys
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import Chrome, ChromeOptions

chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
# Disable JavaScript execution
chrome_options.add_argument('--disable-javascript')
driver = Chrome(options=chrome_options, use_subprocess=True, version_main=114)



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


def generate_file_name(prefix="news"):
    os.makedirs(f"news_detailed/{prefix}", exist_ok=True)
    timestamp = datetime.now().strftime("%H-%M-%S %d-%m-%Y")

    # Define the filename with the timestamp
    filename = f"./news_detailed/{prefix}/{prefix}_{timestamp}.txt"
    print("saving in ", filename)
    return filename


def load_data(file_path):
    # Load the JSON file
    print(f"Loading {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access the loaded data
    return (data)
def get_latest_scraped():
    directory = 'news_detailed/passed'

    latest_file = directory+"/"+max(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)))

    with open (latest_file,'r', encoding='utf-8') as file:
        text = file.readlines()
        return text

def get_images(div_element):
    image_elements = div_element.find_elements(By.XPATH, ".//img")
    prohibited = ['ad.vidverto', 'outbrainimg', 'youtube', 'facebok', 'instagram', 'meta']
    # Process the image elements
    images = []
    image_source = []
    for image_element in image_elements:
        try:
            image_source.append(image_element.get_attribute("src"))
        except:
            pass
    for source in image_source:
        if not any(substr in source for substr in prohibited):
            images.append(source)
    return images


def find_div_with_text(url, text):
    try:
        driver.get(url)
        # page_source = driver.page_source
        data = {}
        # if text in page_source:
        text_xpath = f"//*[contains(text(), '{text}')]/ancestor::div"
        div_element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, text_xpath)))
        article = ""
        src = ""
        images = []
        if div_element:
            try:
                src = driver.current_url.split('www.')[-1].split('/')[0]
            except:
                print("Problem in source website link")
            try:
                images = get_images(div_element)
            except:
                print("Error in getting images")
            try:
                article = get_relatively_long_strings(div_element.text.split('\n'))
            except:
                print("Issue in article")

            data = {
                "source": src if src else "",
                "text": article,
                "images": images
            }
        return data
    except Exception as e:
        print(f"{e}")


def get_detaild_news_from_latest_file(file=None):
    if file:
        data = load_data(file[0])
    else:
        directory = 'news'
        latest_file = max(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        data = load_data(f"news/{latest_file}")
    f_name = generate_file_name(prefix="failed")
    s_name = generate_file_name(prefix="passed")
    with open(f_name, "w", encoding='utf-8') as failed, open(s_name, "w", encoding='utf-8') as news_file:
        for index, d in enumerate(data):
            try:
                print(f"********Going to next page [ {index + 1} of {len(data)} ] **********")
                url = d.get('url')
                text = d.get('title')
                print(url, text)
                # extract_articles(url)
                detail = find_div_with_text(url, text)
                print(detail)
                if detail:
                    news_file.write(f"{detail}\n")
                else:
                    failed.write(f"{d['index']},{d['url']},{d['title']}\n")
                time.sleep(2)
            except Exception as e:
                print(f"{e}")
    driver.quit()
    return {"message": f"Successful files save in news_detailed directory {s_name} and failed in {f_name}"}

    


if __name__ == "__main__":
    arguments = sys.argv[1:]
    get_detaild_news_from_latest_file(arguments)
