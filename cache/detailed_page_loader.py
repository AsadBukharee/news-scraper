from requests_html import HTMLSession
import json

# Create an HTML session
session = HTMLSession()


# Specify the path to the JSON file


def load_data(file_path):
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access the loaded data
    return (data)


def get_content(url, contains_text):
    try:
        # Send a GET request to the webpage
        response = session.get(url)

        # Render JavaScript if needed
        response.html.render()

        # Find the <div> element that contains the specified text
        all_div_tags = response.html.find('div')
        for i,div in enumerate(all_div_tags):
            print(f"----------------------{i+1}------------------------")
            print(div.text)
        # content = target_tag[1].xpath('div')[0].text
        # print(content)
        # return content
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    data = load_data('news/18-51-38 03-06-2023.json')
    for d in data:
        url = d.get('url')
        text = d.get('title')
        print(url, text)
        get_content(url=url, contains_text=text[5:-5])
