from selenium.webdriver.common.by import By
from ScrapingFunctions import *
from AutomationFunctions import *
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
import requests
from dotenv import load_dotenv
import os
from leads.postgresInteraction import PGHandler

load_dotenv()

passcode = os.getenv('POSTGRES_PASSWORD')
email_access_address = os.getenv('EMAIL')
api_key = os.getenv('GOOGLE_MAPS_API_KEY')


class Lead:
    def __init__(self, name, address, phone, website, rating, reviews):
        self.name = name
        self.address = address
        self.phone = phone
        self.website = website
        self.rating = rating
        self.reviews = reviews


class GridCoordinates:
    def __init__(self, ranges, midpoints, search_query):
        self.ranges = ranges
        self.midpoints = midpoints
        self.search_query = search_query

    def section_city(self):
        latitude = self.midpoints["Latitude"]
        longitude = self.midpoints["Longitude"]
        block = (
            f"Grid Cell: \n Latitude Range: {self.ranges['latitude_min']} to {self.ranges['latitude_max']} \n "
            f"Longitude Range: {self.ranges['longitude_min']} to {self.ranges['longitude_max']} \n")
        url = f'https://www.google.com/maps/search/{self.search_query}/@{latitude},{longitude},16z/'

        return block, url


class LeadAcquisition:
    def __init__(self, city_division):
        self.city = input("Give a City and Country Abbreviation (e.g. London, UK): ")
        self.industry = input("Give an Industry (e.g. Dentists): ")
        self.search_query = f"{self.industry} in {self.city}"
        self.api_key = api_key
        self.city_division = city_division
        self.driver = ElementCapture()
        self.driver_actions = self.driver.take_action
        self.database = PGHandler("leads")
        self.database_data = self.database.field_checker("website")

    def acquire_city_urls(self):

        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        payload = {
            "input": self.city,
            "inputtype": "textquery",
            "fields": "geometry",
            "key": self.api_key,
        }

        response = requests.get(url, params=payload)
        data = response.json()
        print(data)
        general_coordinates = data['candidates'][0]['geometry']['viewport']
        northeast = general_coordinates['northeast']
        southwest = general_coordinates['southwest']

        lat_step = (northeast['lat'] - southwest['lat']) / self.city_division
        lng_step = (northeast['lng'] - southwest['lng']) / self.city_division

        grid_coordinates = []

        for row in range(self.city_division):
            for column in range(self.city_division):
                # Calculate the coordinates for the current grid cell
                cell_lat_min = southwest['lat'] + row * lat_step
                cell_lat_max = southwest['lat'] + (row + 1) * lat_step
                cell_lng_min = southwest['lng'] + column * lng_step
                cell_lng_max = southwest['lng'] + (column + 1) * lng_step

                # Append the coordinates of the current grid cell to the list
                grid_math_layout = GridCoordinates(ranges={
                    'latitude_min': cell_lat_min,
                    'latitude_max': cell_lat_max,
                    'longitude_min': cell_lng_min,
                    'longitude_max': cell_lng_max
                },
                    midpoints={
                        "Latitude": (cell_lat_max + cell_lat_min) / 2,
                        "Longitude": (cell_lng_max + cell_lng_min) / 2,

                    }, search_query=self.search_query)
                grid_coordinates.append(grid_math_layout.section_city())

        return grid_coordinates

    def _scrape_lead(self, html):

        aria_label_buttons = lambda string: f'div button[aria-label^="{string}:"]'

        return Lead(name=extract_text(html, 'div h1.DUwDvf.lfPIob'),
                    address=extract_text(html,
                                         f'{aria_label_buttons("Address")} div div div.Io6YTe.fontBodyMedium.kR99db '),
                    phone=extract_text(html,
                                       f'{aria_label_buttons("Phone")} div div div.Io6YTe.fontBodyMedium.kR99db '),
                    website=extract_text(html, 'div a[aria-label^="Website:"]', attributes='href'),
                    rating=extract_text(html, 'div div div div.F7nice span span[aria-hidden="true"]'),
                    reviews=extract_text(html, 'div div div div.F7nice span span span[aria-label*="reviews"]'),
                    )

    def _perform_scrape(self, element):
        """
            Clicks on a given element, opens it in a new tab, and switches focus to the new tab.

            Parameters:
            - driver: An instance of the WebDriverWrapper class.
            - element: The web element to click.
            - initial_window_handle: The window handle before opening the new tab.

            Returns:
            - dict: A dictionary containing the HTML source of the new tab.
            """
        try:

            if isinstance(element, WebElement):
                self.driver.handle_click(element, intricate_scroll=True)

                # After clicking element, scroll down to put next business of view to click without interruption

                for i in range(3):
                    self.driver_actions.send_keys(Keys.ARROW_DOWN).perform()
                page_source = self.driver.firefox_driver.page_source
                html = get_html(page_source)
                return self._scrape_lead(html)

        except ElementClickInterceptedException:
            for i in range(4):
                self.driver_actions.send_keys(Keys.ARROW_DOWN).perform()

    def retrieve_businesses(self, url):
        """
            Retrieves information about businesses from a Google search results page.

            Parameters:
            - driver (WebDriverWrapper): An instance of a custom WebDriverWrapper class for Selenium automation.
            - url (str): The URL of the Google search results page for businesses.



            This function navigates to the specified Google search results page using the provided WebDriver instance.
            It then iterates through different businesses listed on the page, retrieves information such as name, rating,
            reviews, address, phone, and website by clicking on each business link and extracting data from the opened
            window. The information is stored in dictionaries, and the function returns a list containing information
            about multiple businesses.

            Note: The function assumes that there are at least 100 businesses on the search results page.
            """

        self.driver.get_driver().get(url)
        self.driver.get_driver().maximize_window()
        self.driver_actions.send_keys(Keys.RETURN).perform()

        time.sleep(3)

        sorted_elements = self._initiate_infinite_scroll()

        web_elements = [i for i in sorted_elements if isinstance(i, WebElement)]

        if web_elements:
            print(
                f'retrieved {len(web_elements)} elements from the business search and ready to start acquiring data')

            for element in web_elements:
                lead = self._perform_scrape(element)
                self._append_to_database(lead)
                time.sleep(1)
                print(f'appended {lead.name} to json')

        time.sleep(3)
        self.driver.get_driver().quit()

    def _append_to_database(self, lead):
        # Used to Auto Increment IDs
        id_creator = len(self.database_data) + 1 if len(self.database_data) >= 1 else 0

        if not lead.website in self.database_data:
            self.database.insert_to_table(id_creator, lead.name,
                                          lead.website, lead.address, lead.phone,
                                          lead.rating, lead.reviews, None)

    def _initiate_infinite_scroll(self):
        """
            Initiates infinite scrolling on a webpage and captures business elements.
            Created to load every business available to possibly scrape in quadrant

            Parameters:
            - driver: An instance of the WebDriverWrapper class.
            - captured_elements: A set to store unique business elements.

            Returns:
            - bool: True if infinite scroll and element capture succeeded, False otherwise.
            """

        infinite_scroll_elements = self.driver.get_multiple_elements(By.CSS_SELECTOR, 'a.hfpxzc')
        for element in infinite_scroll_elements:
            ActionChains(self.driver.get_driver()).drag_and_drop_by_offset(element, yoffset=300, xoffset=0)
            self.driver.handle_click(element)
            time.sleep(1)

        scroll_count = 1
        while True:
            try:
                # Try to find the end element

                page_source = self.driver.firefox_driver.page_source
                html = get_html(page_source)
                end_of_leads = extract_text(html, 'span span.HlvSq', debug=False)

                # If the end element is found, break the loop
                if end_of_leads is not None and end_of_leads == "You've reached the end of the list.":
                    print(f'scrolled a total of {scroll_count} times. Now scrolling back to the top!')
                    self.driver.scroll_indefinitely(keys='up', multiplier=scroll_count + 1)
                    break
                else:
                    self.driver.scroll_indefinitely(keys='down')
                    scroll_count += 1
            except Exception as e:
                logging.exception(e)
                time.sleep(2)
                self.driver.get_driver().quit()

        # Capture the updated set of elements after scrolling
        different_businesses = self.driver.get_multiple_elements(By.CSS_SELECTOR, 'a.hfpxzc')

        return different_businesses

    def execute(self):
        """
                Executes the main workflow for retrieving business information from Google Maps.

                Parameters:
                - api_key (str): The API key for accessing the Google Places API (default is a placeholder key).
                - driver (ElementCapture): An instance of the ElementCapture class for interacting with web elements (default is a new instance).

                Note: This function takes user input for a search query, retrieves business information, and stores it in a JSON file.
                """

        list_of_url = self.acquire_city_urls()
        max_attempts = 3
        current_attempt = 0
        while current_attempt <= max_attempts:
            try:
                self.bypass_google()
                for idx, (block, url) in enumerate(list_of_url):
                    print(block)
                    self.retrieve_businesses(url)
                    print(f'\n Completed Scrape for Block {idx + 1} Moving to Block {idx + 2} \n')

            except Exception as e:
                logging.exception(e)
                self.driver.get_driver().quit()
                break

    def bypass_google(self):
        """
            Bypasses the Google login page using a WebDriver instance.

            Parameters:
            - url (str): The URL of the Google login page.
            - driver (ElementCapture): An instance of the ElementCapture class for interacting with web elements.
            """

        try:
            self.driver.get_driver().get('https://www.google.co.uk/')
            first_button = self.driver.get_singular_element(By.CLASS_NAME, 'VfPpkd-RLmnJb')

            self.driver.handle_click(first_button)
            # Enter Email Address
            email = self.driver.get_singular_element(By.CLASS_NAME, 'zHQkBf')
            self.driver.handle_click(email)
            self.driver.take_action.send_keys(email)
            self.driver.take_action.send_keys(Keys.ENTER)
            # Wait for the password Webpage to load properly to avoid a stale error
            time.sleep(6)
            # Input Password
            password = self.driver.get_singular_element(By.CSS_SELECTOR, 'input[type="password"]')
            self.driver.handle_click(password)
            self.driver.take_action.send_keys(passcode)
            self.driver.take_action.send_keys(Keys.ENTER)

            # Initiating a long sleep to allow the page to load and also for human touch.
            time.sleep(5)
        except Exception as e:
            logging.exception(e)
            print("Closing Program due to unexpected errors...")
            time.sleep(5)
            self.driver.get_driver().quit()


if __name__ == "__main__":
    programme = LeadAcquisition(city_division=6)
    programme.execute()
