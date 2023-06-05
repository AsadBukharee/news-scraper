import json

from requests_html import HTMLSession

# Create an HTML session
session = HTMLSession()


def load_data(file_path):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access the loaded data
    return (data)



def get_content(url, contains_text):
    # Send a GET request to the webpage
    response = session.get(url)

    # Render JavaScript if needed
    response.html.render()


    # Find the <div> element that contains the specified text
    target_tag = response.html.find('div', first=False, containing=contains_text)
    content = target_tag[1].xpath('div')[0].text
    print(content)
    return content


if __name__ == "__main__":
    contains_text = "قائمة الأهلي - غياب الشناوي وتواجد علي لطفي في ذهاب نهائي أبطال إفريقيا ضد الوداد"
    get_content('https://www.filgoal.com/articles/463524', contains_text)
    print("*****************here we go********************")
    data = load_data('news/18-51-38 03-06-2023.json')
    for d in data:
        url = d.get('url')
        text = d.get('title')
        print(url, text)
        get_content(url="https://www.almasryalyoum.com/news/details/2901883", contains_text=text)
        break
