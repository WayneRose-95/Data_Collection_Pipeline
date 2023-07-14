from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException

# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from urllib3.exceptions import SSLError
from typing import Optional
from time import sleep
import urllib.request
import boto3

# import tempfile
import os
import uuid
import json
import itertools
import requests
import certifi
import logging
import ssl
import mimetypes


#%%

log_filename = "logs/scraper.log"
if not os.path.exists(log_filename):
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)

logger = logging.getLogger(__name__)

# Set the default level as DEBUG
logger.setLevel(logging.DEBUG)

# Format the logs by time, filename, function_name, level_name and the message
format = logging.Formatter(
    "%(asctime)s:%(filename)s:%(funcName)s:%(levelname)s:%(message)s"
)
file_handler = logging.FileHandler(log_filename)

# Set the formatter to the variable format

file_handler.setFormatter(format)

logger.addHandler(file_handler)


class Scraper:

    """
    A class which houses all generic methods for webscraping
    Methods to Add:
    1. Upload_to_S3
    """

    increasing_id = itertools.count()

    def __init__(self):

        chrome_options = ChromeOptions()

        # # chrome_options.add_argument(generate_user_agent())
        # caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9014")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        self.driver = Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )  #

    def land_first_page(self, page_url: str):
        """
        Method to accquire the first page of the website

        parameters:
        page_url : str
        A link which represents the webpage

        """
        home_page = self.driver.get(page_url)
        logger.debug("Landed first page")
        return home_page

    def accept_cookies(self, cookies_button_xpath: str, iframe: Optional[str] = None):

        """
        Method to click the accept_cookies button on the webpage

        Parameters:
        cookies_button_xpath : str
        A string which represents the web_element for the accept_cookies button

        iframe: Optional[str]:
        An optional parameter which can be called in case the button is within
        an iframe.

        """
        sleep(4)
        try:
            if iframe:  # To find if the accept cookies button is within a frame
                cookies_iframe = self.driver.find_element(By.ID, iframe)
                self.driver.switch_to.frame(cookies_iframe)
                accept_cookies_button = (
                    WebDriverWait(self.driver, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, cookies_button_xpath))
                    )
                ).click()
            else:
                accept_cookies_button = (
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, cookies_button_xpath))
                    )
                ).click()
            logger.debug("The accept cookies button has been clicked")

        except NoSuchFrameException:  # If it is not within a frame then find the xpath and proceed click it.
            logger.warning("No iframe found")
            accept_cookies = self.driver.find_element(By.XPATH, cookies_button_xpath)
            accept_cookies.click()
            logger.debug("The accept cookies button has been clicked")
        return True

    def _look_for_search_bar(self, search_bar_xpath: str):

        """
        Method to look for a search bar on the webpage

        Parameters:

        search_bar_xpath : str
        A string which represents the web-element for the search bar on the webpage

        Returns:
        search_bar_element:
        A web-element representing the search bar on the webpage

        """
        try:
            search_bar_element = WebDriverWait(self.driver, 0.5).until(
                EC.presence_of_element_located((By.XPATH, search_bar_xpath))
            )
            # Click on the element for the search bar
            search_bar_element.click()
        except:
            # If it is not present, close the window.
            logger.exception("no search bar found")

        return search_bar_element

    def _send_keys_to_search_bar(self, search_bar_xpath: str, text: str):
        """
        Method to look for a search bar on the webpage

        Parameters:

        search_bar_xpath : str
        A string which represents the web-element for the search bar on the webpage

        text : str
        The text which the user wants to put into the search bar i.e. "text"

        Returns:
        search_bar_element:
        A web-element representing the search bar on the webpage

        """
        search_bar_element = self.look_for_search_bar(search_bar_xpath)

        if search_bar_element:
            search_bar_element.send_keys(text)
            search_bar_element.send_keys(Keys.ENTER)
        else:
            logger.exception("Text failed")
            raise Exception

        return text

    def _infinite_scroll_down_page(self):

        SCROLL_PAUSE_TIME = 5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def extract_page_links(
        self, container_xpath: str, attribute: str = "href" or "src" or "alt" or "title"
    ):

        try:
            # find the container with the links
            page_container = WebDriverWait(self.driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, container_xpath))
            )

        except Exception:
            logger.exception("entered exception")

        self.page_links_list = []

        page_counter = 0
        # iterate through these links
        for url in page_container:
            link_to_page = url.get_attribute(attribute)
            self.page_links_list.append(link_to_page)
            page_counter += 1

        # For a sanity check, print the list of links and the number of pages

        print(f"Pages visited: {len(self.page_links_list)}")
        return self.page_links_list

    def _click_button_on_page(self, button_xpath):
        return self.driver.find_element(By.XPATH, button_xpath).click()

    def collect_number_of_pages(self, last_page_number_selector: str):
        try:
            last_page_number_element = self.driver.find_element(
                By.CSS_SELECTOR, last_page_number_selector
            ).text
            logger.debug(last_page_number_element)
            logger.info(f"Max Page = {last_page_number_element}..")
            last_page_number = int(last_page_number_element)
        except NoSuchElementException:
            logger.exception("Element not found. Exiting...")

        return last_page_number

    def _find_container(self, container_xpath: str):
        try:
            container = self.driver.find_element(By.XPATH, container_xpath)
            print(container)
        except:
            logger.exception("There was no element. Please check your xpath")
            raise Exception

    def _apply_filter_list(self, filter_container_xpath: str, filter_button=None):

        """
        Method to work with the filter lists on a webpage.

        Parameters:

        filter_container_xpath : str

        A string which represents the web-element for the filter container on the page

        filter_button = None
        A string which represents the web-element for the filter button on the page

        """
        if filter_button:
            filter_button = self.driver.find_element(By.XPATH, filter_button)
            filter_button.click()

            # filter_container = self.extract_the_page_links('//ul[@class="dropdown dropdown_open"]//li/a', 'href')
            filter_container = self.driver.find_elements(
                By.XPATH, filter_container_xpath
            )
            filter_container_list = []

            for url in filter_container:
                link_to_page = url.get_attribute("href")
                filter_container_list.append(link_to_page)
            print(filter_container_list)
        else:

            # filter_container = self.extract_the_page_links('//ul[@class="dropdown dropdown_open"]//li/a', 'href')
            filter_container = self.driver.find_elements(
                By.XPATH, filter_container_xpath
            )
            filter_container_list = []

            for url in filter_container:
                link_to_page = url.get_attribute("href")
                filter_container_list.append(link_to_page)

            print(filter_container_list)
            return filter_container_list

    def _download_image(self, image_xpath: str, game_category: str, game_name: str):

        """
        Method to download the image from the webpage

        Parameters:
        image_xpath : str
        A string which represents the web element of the image on the webpage
        e.g.
        '//*[@id="product-gallery"]/div[2]/div[2]/div[2]/img'

        game_category : str
        The category which the game is in i.e. Action, Adventure, RPG etc.

        Game_Name : str
        A string representing the name of the game being downloaded
        """
        image_category = game_category
        image_name = f"{game_name}-{game_category}-image"
        src_list = self.extract_page_links(image_xpath, "src")
        # //*[@id="product-gallery"]/div[2]/div[2]/div[2]/img

        try:
            image_path = f"images/{image_category}"
            sslcert = ssl._create_default_https_context(cafile=certifi.where())
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            for i, src in enumerate(src_list):
                imagerequest = requests.get(src, stream=True)
                gameimage = open(f"{image_path}/{image_name}.{i}.jpg", "wb")
                for chunk in imagerequest.iter_content(1024):
                    gameimage.write(chunk)
                # Guess the image type using mimetypes library. Return the first element of the tuple.
                check_image_type = mimetypes.guess_type(
                    f"{image_path}/{image_name}.{i}.jpg"
                )[0]
                logger.debug(f"Image type is {check_image_type}")
                gameimage.close()
                logger.info(
                    f"Game image for {game_name} is now avaliable in image path."
                )
                # TODO: Import mimetypes and validate the image file
            return check_image_type

        except SSLError:
            ssl._create_default_https_context(cafile=certifi.where())
            for url in src_list:
                url.replace("https", "http")
                image_path = f"images/{image_category}"
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            for i, src in enumerate(src_list):
                urllib.request.urlretrieve(src, f"{image_path}/{image_name}.{i}.jpg")
            # Guess the image type using mimetypes library. Return the first element of the tuple.
            check_image_type = mimetypes.guess_type(
                f"{image_path}/{image_name}.{i}.jpg"
            )[0]
            logger.debug(f"Image type is {check_image_type}")
            return check_image_type

    def _set_s3_connection(self):
        """
        Method to create service client connection to the S3 AWS services.
        Returns:
            self.s3_client: variable name for the s3 client connection
        """
        self.s3_client = boto3.client("s3")
        return self.s3_client

    def _save_image_links(self, sub_category_name: str, image_container_xpath: str):
        """
        Method to download every product image (jpg format).

        Parameters:
            sub_category_name (str): The name of the sub-category
            image_container_xpath (str): The name of the container for the xpaths
        """

        # TODO: The scraper breaks on random pages when it tries to get images. Why?

        image_srcs = self.extract_the_page_links(image_container_xpath, "src")
        sub_category_name = self.extract_the_page_links(image_container_xpath, "alt")

        while len(sub_category_name) > 0:
            image_string = sub_category_name.pop(0)
            strip_irregular_characters = image_string.replace(":", "")
            image_name = strip_irregular_characters[:200]
            logger.info(f"Image name stripped from list")

        while len(image_srcs) > 0:
            image_link = image_srcs.pop(0)
            logger.info(f"Image link stripped from list")

        image_dict = {}

        self.image_xpath_dict = {
            "UUID": "",
            "Image_Name": f"{image_name}",
            "Image_Link": [f"{image_link}"],
        }

        for key, value in self.image_xpath_dict.items():
            try:
                if key == "UUID":
                    image_dict[key] = str(uuid.uuid4())
                elif key == "Image_Link":
                    image_dict[key] = value
                else:
                    image_dict[key] = value
            except:
                image_dict[key] = "Null"

        logger.debug(image_dict)
        return image_dict

    def save_json(self, all_products_dictionary: list or dict, sub_category_name: str):
        """
        Method to save the products into a .json format

        Parameters:
        all_products_dictionary : list or dict
        A dictionary or list representing the data to be converted

        sub_category_name : str
        The name of the .json file the user wants to give to the .json file.

        Returns:
        True : Bool
        If the .json file has been created.


        """
        file_to_convert = all_products_dictionary
        file_name = f"{sub_category_name}-details.json"
        # Logic for uploading to cloud servers.
        # If the user sets s3_upload to True, perform the following:

        if not os.path.exists("json-files"):
            os.makedirs("json-files")
        with open(f"json-files/{file_name}", mode="a+", encoding="utf-8-sig") as f:
            json.dump(file_to_convert, f, indent=4, ensure_ascii=False)
            f.write("\n")
        logger.debug(".json file created locally.")

        return True


#%%

if __name__ == "__main__":
    bot = Scraper()
