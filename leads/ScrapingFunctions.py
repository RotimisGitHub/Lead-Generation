import json
import logging
import requests
from selectolax.parser import HTMLParser
import re
from random import choices
import os


def get_html(response):
    """
        Parses the HTML content from a given response.

        Parameters:
        - response (str): The HTML response from a web page.

        Returns:
        - HTMLParser: An instance of the HTMLParser class.
        """
    html = HTMLParser(response)
    return html


def extract_text(html, selector: str, debug=False, attributes=None, multiple=False):
    """
        Extracts text content from HTML using a CSS selector.

        Parameters:
        - html (HTMLParser): An instance of the HTMLParser class.
        - selector (str): CSS selector to locate the desired element.

        Returns:
        - str: The extracted text content or None if no matching element is found.
        """
    try:
        if not multiple:
            if not attributes:
                text = html.css_first(selector).text
                return text
            else:
                assured_attributes = html.css_first(selector).attributes[attributes]
                return assured_attributes
        else:
            if not attributes:
                text_list = html.css(selector)
                text = [i.text for i in text_list]
                return text
            else:
                attributes_list = []
                assured_attributes = html.css(selector)
                for i in assured_attributes:
                    attributes_list.append(i.attributes[attributes])
                return attributes_list

    except AttributeError:
        if debug:
            logging.exception(
                f"Attribute Error: NoneType: No matching element found for selector: {selector} because selector is a {type(selector)} type.")

        return None
    except Exception as e:
        logging.exception(f"Error extracting text with selector {selector}: {str(e)}")
        return None


def clean_data(data: str):
    """
        Cleans and formats text data by removing unnecessary characters.

        Parameters:
        - data (str): The raw text data to be cleaned.

        Returns:
        - str: The cleaned and formatted text data.
        """
    text = data.replace("\n", "")
    cleaned_string = re.sub(' +', ' ', text).strip()
    if not data[0].isalpha() and not data[-1].isalpha():
        cleaned_string.replace(data[0], '')
        cleaned_string.replace(data[-1], '')
    return cleaned_string


def get_webpage(url: str, search_params, pages):
    """
        Retrieves the HTML content of a webpage using the provided URL and search parameters.

        Parameters:
        - url (str): The URL of the webpage.
        - search_params (str): Additional search parameters to be appended to the URL.
        - pages (int): Number of pages to retrieve.

        Returns:
        - requests.Response: The response object containing the HTML content.
        """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/83.0.4254.66",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
    ]

    random_agent = ''.join(choices(user_agents))

    headers = {
        "User-Agent": random_agent
    }
    if search_params:
        response = requests.get(url=(url + search_params) + pages, headers=headers)
    else:
        response = requests.get(url=url, headers=headers)

    return response


def cookie_jar(text_file: str):
    """
       Reads cookie information from a text file and returns a list of dictionaries.

       Parameters:
       - text_file (str): The path to the text file containing cookie information.

       Returns:
       - List[dict]: A list of dictionaries representing cookies.
       """
    with open(text_file, 'r') as cookies:
        cookie = cookies.read().split(';')
    cookies_and_value = [i.split("=") for i in cookie]
    final_cookie_jar = []
    for i in cookies_and_value:
        name = i[0].strip()
        value = i[1].strip()
        final_cookie_jar.append(
            {"name": name,
             "value": value}
        )
    return final_cookie_jar


def add_to_json(data, filename: str, dir_name=None):
    # Create the directory if it doesn't exist
    full_path = os.path.join(os.getcwd(), dir_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    file_path = os.path.join(full_path, f'{filename}.json')

    # Check if the file exists
    if os.path.exists(file_path):
        # Load existing data from the file
        with open(file_path, 'r', encoding='UTF-8') as file:
            existing_data = json.load(file)
    else:
        # If the file doesn't exist, initialize with an empty list
        existing_data = []

    if data not in existing_data:
        # Append new data to the existing data
        existing_data.append(data)

        # Write the data to the file
        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
    else:
        print("Data Already Exists in JSON File")

    return True
