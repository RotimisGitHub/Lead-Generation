import time
import io
import logging
import speech_recognition
from selenium.webdriver.common.by import By
from ScrapingFunctions import *
from AutomationFunctions import *
import json
import base64
from PIL import Image
import pytesseract
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from vpnJumper import *


def get_all_website_urls(filename):
    with open(filename, 'r') as data:
        json_data = json.load(data)

        web_urls = []
        for business in json_data:
            if business and business['Website']:
                if 'Email Addresses' not in business and 'Social Platforms' not in business:
                    websites = business['Website']
                    site_name = business["Name"]
                    web_urls.append({"Name": site_name,
                                     "Website": websites})

    print(web_urls)

    return web_urls


def _take_screenshot(driver):
    page_img = driver.get_driver().get_screenshot_as_base64()
    image_data = base64.b64decode(page_img)
    image = Image.open(io.BytesIO(image_data))
    page_text = pytesseract.image_to_string(image)
    return page_text


def create_search_queries(web_urls: list, site_query, social_media_searches, contact_search):
    search_book = []
    for website in web_urls:
        raw_url = str(website['Website'])
        if "http://" in raw_url:
            usable_url = raw_url.split("http://")[-1]
        elif "https://":
            usable_url = raw_url.split("https://")[-1]
        url = usable_url.split('/')[0]
        dictionary_terms = {
            "website": website['Website'],
            "Media Search": site_query + url + social_media_searches,
            "Contact Details Search": site_query + usable_url + contact_search
        }

        search_book.append({"Business": website["Name"],
                            "Search Terms": dictionary_terms})

    print(search_book)
    return search_book


def _acquire_page_source(driver, vpn):
    element = driver.get_singular_element(By.CSS_SELECTOR, "a[jsname='UWckNb']")
    driver.handle_click(element, open_tab=True)
    vpn.disconnect()
    list_of_handles = driver.get_driver().window_handles
    next_window = list_of_handles[-1]
    driver.get_driver().switch_to.window(next_window)  # Switch to the last window handle
    print('Now on page: ', driver.get_driver().title)
    driver.get_driver().refresh()
    time.sleep(2)

    page_source = driver.firefox_driver.page_source
    html = get_html(page_source)
    return html


def solve_captcha(driver):
    print("We have a recaptcha")
    # Wait for the window to be available to we can switch to tht iframe
    wait = WebDriverWait(driver.get_driver(), 10)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, ".//iframe[@title='reCAPTCHA']")))

    # Click the Check Box
    checkButton = driver.get_singular_element(By.ID, "recaptcha-anchor-label")
    driver.handle_click(checkButton)

    # To be able to select the challenge we need to switch in and out of the default frame
    driver.get_driver().switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        (By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']")))

    # Select the Audio option
    audioOption = driver.get_singular_element(By.ID, "recaptcha-audio-button")
    driver.handle_click(audioOption)

    # Ue transcribe function to transform the audio file to text
    text = _transcribe(driver.get_driver().find_element(By.ID, "audio-source").get_attribute('src'))
    response_box = driver.get_singular_element(By.ID, "audio-response")
    driver.send_keys_to_target(response_box, text=text)
    submitResponse = driver.get_singular_element(By.ID, "recaptcha-verify-button")
    driver.handle_click(submitResponse)
    print(f"Sent {text} to captcha and was successful!")
    return True


def _transcribe(url):
    os.environ[
        'GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/rotimi_jatto/PycharmProjects/Proper_Projects/Google_scraping/leads/service_account.json'
    sr = speech_recognition.Recognizer()
    audioData = speech_recognition.AudioData(requests.get(url).content, 44100, 2)
    text = sr.recognize_google_cloud(audioData)
    return text


def initiate_searches(driver, search_query, vpn):
    search_bar = driver.get_singular_element(By.CSS_SELECTOR, "textarea.gLFyf")
    driver.send_keys_to_target(search_bar, search_query, submit=True)
    vpn.establishConnection()
    driver.get_driver().refresh()
    time.sleep(5)
    current_window = driver.get_driver().current_window_handle

    # Check to see if there are any search results, if not then move on
    # Check if there is a recaptcha

    page_text = _take_screenshot(driver)

    zeroResults = r'About 0 results'
    badSpelling = r'Make sure that all words are spelled correctly'
    recaptchaAlert = (
        r"Our systems have detected unusual traffic from your computer network. This page checks to see if it's "
        r"really you sending the requests, and not a robot. Why did this happen?")

    if zeroResults not in page_text:
        if badSpelling not in page_text:
            print("We have acquired Results!")
            page_source = driver.firefox_driver.page_source

            html2 = _acquire_page_source(driver, vpn)
            html1 = get_html(page_source)

            return {"html": (html1, html2),
                    "Initial Window": current_window}
        else:
            print("There are no results for this business. Moving to the next!")
            return None
    elif recaptchaAlert in page_text:
        captcha = solve_captcha(driver)
        if captcha:
            time.sleep(5)
            page_source = driver.firefox_driver.page_source
            html2 = _acquire_page_source(driver, vpn)
            html1 = get_html(page_source)

            return {"html": (html1, html2),
                    "Initial Window": current_window}

    else:
        print("There are no results for this business. Moving to the next!")
        return None


def initiate_media_scraping(html):
    # Need to make a function in scraping functions
    # that looks for certain texts in a site and returns attributes concerning it
    social_platforms = ['instagram', 'twitter', 'facebook', 'linkedin', 'youtube', 'wa.me']

    all_hyperlinks = []
    for page_sources in html:
        hyperlinks = extract_text(page_sources, selector='a', attributes="href", multiple=True)
        all_hyperlinks.append(hyperlinks)

    confirmed_social_pages = []
    for media in social_platforms:
        social_media_links = [link for link in all_hyperlinks if media in link]
        if social_media_links:
            platform_dict = {
                media: list(set(social_media_links)),
            }
            confirmed_social_pages.append(platform_dict)

    return {"Social Platforms": confirmed_social_pages}


def initiate_contact_scraping(html: HTMLParser):
    # Need to make a function in scraping functions
    # that looks for certain texts in a site and returns attributes concerning it
    all_links = extract_text(html, selector='a', attributes="href", multiple=True)
    body = extract_text(html, selector='body', multiple=True)

    emails_found = []
    if all_links is not None:

        for links in all_links:
            if "@" in links:
                if "mailto:" in links:
                    links = str(links).split("mailto:")[1]
                elif "?" in links:
                    links = str(links).split("?")[0]
                emails_found.append(links)
    else:
        emails_found.append('None')

    if body is not None:
        for links in body:
            if "@" in links:
                if ".com" or ".co.uk" or "org.uk" in links:
                    emails_found.append(links)
    else:
        emails_found.append('None')

    emails_found.remove('None')

    print('Emails Found: ', list(set(emails_found)))

    if emails_found is None:
        return {"Email Addresses": None}
    else:
        return {"Email Addresses": list(set(emails_found))}


def initiate_about_scraping():
    # Purpose is to look for keywords and phrases to see if service offers what we are looking for
    # can use images of the entire site as well as text
    # get all data and see if our search terms are within the site
    # Look through entire body of the page for text and images
    # We will also analyse the text on the about page within 100 words to get a grasp of what they're about in general
    pass


def _append_data_to_json(scraped_data: dict, selected_business, filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)

        for entry in data:
            if entry.get('Name') == selected_business:
                entry.update(scraped_data)
                break

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")


def start_social_search(driver, search_queries, business_name, filename, vpn):
    valid_webpage = initiate_searches(driver, search_queries, vpn)
    if valid_webpage is not None:

        social_platforms = initiate_media_scraping(valid_webpage["html"])
        print(social_platforms)
        _append_data_to_json(scraped_data=social_platforms, selected_business=business_name, filename=filename)
        time.sleep(2)

        return True
    else:
        return None


def start_contact_search(driver, search_queries, business_name, filename, vpn):
    valid_webpage = initiate_searches(driver, search_queries, vpn)
    if valid_webpage is not None:
        contact_information = initiate_contact_scraping(valid_webpage["html"])
        print(contact_information)
        _append_data_to_json(scraped_data=contact_information, selected_business=business_name, filename=filename)
        time.sleep(2)

        return True
    else:
        return None


def execution(driver=ElementCapture(), vpn=VPNJumper(country="United States")):
    filename = 'extracted_leads/Dentists_in_London_UK.json'
    web_list = get_all_website_urls(filename)

    site_query = 'site: '
    social_media_searches = r' "instagram" OR "twitter" OR "facebook" OR "tiktok" OR "linkedin" OR "Youtube"'
    contact_search = r' "contact us"'

    search_book = create_search_queries(web_urls=web_list, site_query=site_query,
                                        social_media_searches=social_media_searches, contact_search=contact_search)
    driver.get_driver().get("https://www.google.com/")
    driver.get_driver().maximize_window()
    time.sleep(2)
    rejectSignIn = driver.get_singular_element(By.ID, "W0wltc")
    driver.handle_click(rejectSignIn)

    try:

        for site in search_book:
            start_social_search(driver, site["Search Terms"]["Media Search"], site["Business"], filename, vpn)
            start_contact_search(driver, site["Search Terms"]["Contact Details Search"], site["Business"], filename, vpn)

        driver.get_driver().quit()

    except Exception as e:
        logging.exception(e)
        driver.get_driver().quit()


if __name__ == "__main__":
    execution()
