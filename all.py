from collections import Counter

import requests
from bs4 import BeautifulSoup
import numpy as np
from scipy.stats import zscore

def get_useful_strings(string_list, min_word_count_threshold=3, zscore_threshold=1):
    word_counts = np.array([len(string.split()) for string in string_list])
    zscores = zscore(word_counts)

    filtered_strings = [string for string, zscore_val in zip(string_list, zscores) if len(string.split()) >= min_word_count_threshold and zscore_val >= zscore_threshold]

    return filtered_strings
def get_text(url):
    try:
        response = requests.get(url)
        if response.status_code==200:
            # parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # find all parent tags that contain one or more <p> tags
            parent_tags = soup.find_all('div')

            # determine which parent tag has the most <p> tags
            max_p_tag_count = 0
            max_p_tag = None

            for parent_tag in parent_tags:
                p_tag_count = len(parent_tag.find_all('p'))
                if p_tag_count > max_p_tag_count:
                    max_p_tag_count = p_tag_count
                    max_p_tag = parent_tag

            # print the tag with the most <p> tags
            text_chunks = max_p_tag.text.split('\n')
            # counts = Counter(text_chunks).values()
            # print (counts)
            useful = get_useful_strings(string_list=text_chunks)
            if not useful:
                return max_p_tag.text

            return useful
        return "This site is blocked in your area or access not granted"
    except Exception as e:
        print(f"{e}")
        return "This site is blocked in your area or access not granted"


if __name__=="__main__":
    while (True) :
        print(get_text(input("\n\nPlease enter url :")))