import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import Chrome, ChromeOptions

from load_all_news_detail import get_images, get_relatively_long_strings

chrome_options = ChromeOptions()
# chrome_options.headless=True
# chrome_options.add_argument('--headless')
# Disable JavaScript execution
chrome_options.add_argument('--disable-javascript')
driver = Chrome(options=chrome_options, use_subprocess=True, version_main=114)


# driver.patcher.version_main=114


def find_div_with_text(url, text):
    try:
        driver.get(url)
        # page_source = driver.page_source
        data = {}
        # if text in page_source:
        text_xpath = f"//*[contains(text(), '{text}')]/ancestor::div"
        div_element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, text_xpath)))
        print("Text found 🥳")
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


def load_failed():
    directory = "news_detailed/failed"
    latest_failed_links_file = directory + "/" + max(os.listdir(directory),
                                                     key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    with open(latest_failed_links_file, 'r',encoding='utf-8') as file:
        lines = file.readlines()
    if lines:
        passed_file = latest_failed_links_file.replace('failed', 'passed')
        with open(passed_file, 'a',encoding='utf-8') as update:
            for i, line in enumerate(lines):
                print(f"Scraping {i+1} of {len(lines)}")
                [index, url, title] = line.split(',')
                detail = find_div_with_text(url, title)
                print(detail)
                if detail:
                    update.write(f"{detail}\n")
                    del lines[i]
                time.sleep(2)

        with open(latest_failed_links_file, 'w') as update:
            for i, line in enumerate(lines):
                update.write(line + "\n")
    else:
        print("No failed url found 🎉🥳🎊")


if __name__ == "__main__":
    load_failed()
    driver.quit()
