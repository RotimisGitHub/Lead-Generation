import logging
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from random import randint, choice
import time


class CustomWebdriver:
    """
        CustomWebdriver class for managing the WebDriver instance with specific configurations.

        Attributes:
        - service (ChromeService): The Chrome service for WebDriver.
        - options (webdriver.ChromeOptions): Options for configuring the Chrome browser.
        - firefox_driver (webdriver.Chrome): The main WebDriver instance.

        Methods:
        - get_driver(): Returns the main WebDriver instance.

        Note: This class initializes the WebDriver with specific options and settings.
        """

    def __init__(self):
        self.service = FirefoxService('/usr/local/bin/geckodriver')
        self.options = webdriver.FirefoxOptions()

        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; Pixel 3a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 YaBrowser/20.2.1.187 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.4.14 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.320 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Edg/79.0.309.43",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Edg/79.0.309.43",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Edg/78.0.276.19",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 YaBrowser/19.12.4",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 Edg/79.0.309.43",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.4.14 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Edg/79.0.309.43",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Edg/78.0.276.19",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 YaBrowser/19.12.4.14 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/64.0.3417.92",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36 OPR/64.0.3417.92",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 Edg/79.0.309.43",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.4.14 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Edg/79.0.309.43",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 Edg/78.0.276.19",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 YaBrowser/19.12.4.14 Yowser/2.5 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36 OPR/64.0.3417.92",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36 OPR/64.0.3417.92",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108"

        ]
        user_agent = choice(user_agents)

        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        # self.options.headless = True
        # self.options.add_argument('--headless')
        # Exclude the collection of enable-automation switches
        # self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # Turn-off userAutomationExtension
        # self.options.add_experimental_option("useAutomationExtension", False)

        self.firefox_driver = webdriver.Firefox(service=self.service, options=self.options)
        self.firefox_driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def get_driver(self):
        """
                Returns the main WebDriver instance.

                Returns:
                - webdriver.Chrome: The main WebDriver instance.
                """
        return self.firefox_driver


class ElementCapture(CustomWebdriver):
    """
        ElementCapture class for interacting with web elements using Selenium.

        Attributes:
        - randomized_time (int): Randomized time for adding delays.
        - driver (webdriver.Chrome): The main WebDriver instance.
        - element: The web element to be interacted with.
        - take_action (ActionChains): ActionChains instance for performing actions on web elements.

        Methods:
        - get_singular_element(code_format, value): Retrieves a single web element based on the provided code_format and value.
        - get_multiple_elements(code_format, value): Retrieves multiple web elements based on the provided code_format and value.
        - get_and_manipulate_element(code_format, value, retrieved_element, action, text, submit): Interacts with a web element.
        - scroll(retrieved_element, code_format, value, use_element, amount): Scrolls the page or to a specific element.

        Note: This class extends CustomWebdriver and provides methods for interacting with web elements.
        """

    def __init__(self):
        super().__init__()  # Initialize CustomWebdriver if not provided

        self.randomized_time = randint(2, 5)
        self.driver = self.get_driver()
        self.take_action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)

    def get_singular_element(self, code_format, value):
        """
               Retrieves a single web element based on the provided code_format and value.

               Parameters:
               - code_format (str): The format used to locate the web element (e.g., By.CSS_SELECTOR).
               - value (str): The value associated with the code_format for locating the web element.

               Returns:
               - list: A list containing the retrieved web element(s).
               """

        self.element = self.wait.until(
            EC.presence_of_element_located((code_format, value))
        )
        print(f"successfully retrieved element")

        return self.element

    def get_multiple_elements(self, code_format, value):
        """
                Retrieves multiple web elements based on the provided code_format and value.

                Parameters:
                - code_format (str): The format used to locate the web element (e.g., By.CSS_SELECTOR).
                - value (str): The value associated with the code_format for locating the web element.

                Returns:
                - list: A list containing the retrieved web element(s).
                """

        try:

            self.element = self.wait.until(
                EC.presence_of_all_elements_located((code_format, value))
            )
            print(f"successfully retrieved {len(self.element)} elements")

            return self.element

        except BaseException as e:
            self._handle_exception(e)

    def handle_click(self, retrieved_element, scroll=True, open_tab=False, intricate_scroll=False):
        self.element = retrieved_element

        try:
            time.sleep(self.randomized_time)
            if scroll is True:
                self.take_action.scroll_to_element(self.element)

            if intricate_scroll:
                for i in range(1, 5):
                    self.take_action.send_keys(Keys.DOWN)

            if open_tab:
                self.take_action.key_down(Keys.COMMAND).perform()
                self.element.click()
                self.take_action.key_up(Keys.COMMAND).perform()
                print('opened new window through element')
            else:
                self.element.click()
                print(f"successfully clicked on element")

        except TimeoutException:

            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
            self.driver.execute_script("arguments[0].click();", self.element)

            print(f"successfully clicked on element using javascript!")

    def send_keys_to_target(self, retrieved_element, text: str, submit=False, scroll=True):
        self.element = retrieved_element
        try:
            time.sleep(self.randomized_time)
            if scroll:
                _initiate_movement(self.take_action, self.driver, self.element)
            else:
                pass
            self.element.clear()
            for i in text:
                self.element.send_keys(i)
                random_float = randint(1, 3) / 10
                time.sleep(random_float)
            print(f"successfully sent keys: {text} to element")
            if submit:
                time.sleep(2)
                self.element.send_keys(Keys.RETURN)
                print(f"Successfully submitted keys and awaiting next step!")
            else:
                pass
        except Exception as e:
            self._handle_exception(e)

    def scroll_to_element(self, retrieved_element, multiplier=None):
        """
                Scrolls the page or to a specific element.

                Parameters:
                - retrieved_element (WebElement): A pre-existing web element to scroll to (optional).
                - code_format (str): The format used to locate the web element (used when retrieved_element is not provided).
                - value (str): The value associated with the code_format for locating the web element (used when retrieved_element is not provided).
                - use_element (bool): Whether to use a pre-existing web element for scrolling.
                - amount (int): The amount to scroll (used when use_element is False).

                Note: If use_element is True, it scrolls to the specified pre-existing element; otherwise, it scrolls
                      the page by the specified amount.
                """

        try:
            self.element = retrieved_element

            time.sleep(self.randomized_time)

            if multiplier:
                _initiate_movement(self.take_action, self.driver, self.element, multiplier=multiplier)
            else:
                _initiate_movement(self.take_action, self.driver, self.element)
            print(f"successfully scrolled to element")
        except BaseException as e:
            self._handle_exception(e)

        try:

            _initiate_movement(self.take_action, self.driver, self.element)
            print(f"successfully scrolled")

        except BaseException as e:
            self._handle_exception(e)

    def scroll_indefinitely(self, amount=None, keys=None, multiplier=1):

        try:

            time.sleep(2)
            if amount:
                _initiate_movement(self.take_action, self.driver, amount=amount)

            elif keys == "down":
                for i in range(1, multiplier + 1):
                    self.take_action.send_keys(Keys.END).perform()
                    time.sleep(0.5)
            elif keys == "up":
                for i in range(1, multiplier + 1):
                    self.take_action.send_keys(Keys.PAGE_UP).perform()
                    time.sleep(0.5)


        except BaseException as e:
            self._handle_exception(e)
        except ZeroDivisionError as e:
            print("Didn't move at all. Closing program.")
            self._handle_exception(e)

    def set_mouse_to_middle(self, on=True):
        if on:
            window_width = self.driver.execute_script("return window.innerWidth;")
            window_height = self.driver.execute_script("return window.innerHeight;")

            middle_x = window_width / 2
            middle_y = window_height / 2
            self.take_action.move_by_offset(middle_x, middle_y).perform()

    def _handle_exception(self, e):
        logging.exception(e)
        time.sleep(self.randomized_time)
        self.driver.quit()


def _initiate_movement(actions, driver, element=None, multiplier=None, amount=None):
    """
        Initiates the scrolling movement based on the specified amount.

        Parameters:
        - amount (int): The amount to scroll.
        - actions (ActionChains): ActionChains instance for performing scrolling actions.
        - driver (webdriver.Chrome): The main WebDriver instance.

        Note: This is a helper function used internally in the ElementCapture class for scrolling.
        """
    if amount is None and element:
        current_position = \
            driver.execute_script("return { x: window.pageXOffset, y: window.pageYOffset };")['y']
        element_position = element.location['y']
        total_movement = element_position - current_position

        amount = total_movement if multiplier is None else total_movement * int(multiplier)
    else:

        global divider
        try:

            if 1000 > amount > 600:
                divider = 6
            elif 600 > amount > 200:
                divider = 4
            elif amount > 1000:
                divider = 10
            elif amount == 0 or amount is None:
                divider = 1
            else:
                divider = 1

            for i in range(1, int(amount), int(amount / divider)):
                actions.scroll_by_amount(delta_x=0, delta_y=int(i)).perform()
                time.sleep(0.2)

        except BaseException as e:
            logging.exception(e)
            time.sleep(3)
            driver.quit()
