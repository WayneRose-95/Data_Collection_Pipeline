import time
import os
from numpy import number
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from urllib3 import Timeout
from ScraperClass import Scraper
from data_cleaning import DataCleaning
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

# from alive_progress import alive_bar
import uuid
import logging


log_filename = "logs/metacritic_scraper.log"
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


class MetaCriticScraper(Scraper):

    """
    A class which scrapes all of the fighting games off of the site metacritic.com

    Parameters:

    url (str):
    The url of the site which you wish to visit

    """

    def __init__(self, url):
        super().__init__()

        try:
            self.driver.set_page_load_timeout(30)
            self.land_first_page(url)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
            self.driver.quit()

        self.page_counter = 0

        # TODO: Adjust the keys of the self.xpaths_dict to take the headings from the pages.
        self.xpaths_dict = {
            "UUID": "",
            "Title": '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a/h1',
            "Link_to_Page": '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a',
            "Platform": '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/span',
            "Release_Date": '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[3]/ul/li[2]/span[2]',
            "MetaCritic_Score": '//a[@class="metascore_anchor"]/div',
            "User_Score": '//div[@class="userscore_wrap feature_userscore"]/a/div',
            "Developer": '//li[@class="summary_detail developer"]/span[2]/a',
            "Description": './/li[@class="summary_detail product_summary"]',
        }

    def accept_cookies(self, cookies_button_xpath: str):
        return super().accept_cookies(cookies_button_xpath)

    def choose_category(self, category_selection: str = "game" or "music"):

        """
        Currently works for games and music pages
        """

        # List of hrefs to visit
        href_list = ["https://www.metacritic.com/game"]
        if category_selection == "game":
            try:
                self.driver.get(href_list[0])
            except TimeoutException:
                self.driver.refresh()
                time.sleep(3)
                self.driver.get(href_list[0])

        logger.info(f"Navigating to: {category_selection}")
        return category_selection

    def choose_genre(self):

        """
        Currently works for games, tv and music
        """
        genre_container = self.driver.find_elements(
            By.XPATH, '//ul[@class="genre_nav"]//a'
        )

        list_of_genre_links = []
        list_of_genres = []
        for item in genre_container:
            list_of_genre_links.append(item.get_attribute("href"))
            list_of_genres.append(item.text)

        logger.info(list_of_genre_links)
        logger.info(f"Here are the list of genres: {list_of_genres}")
        return list_of_genre_links

    def click_next_page(self, page):

        next_page_element = self.driver.find_element(
            By.XPATH,
            f'//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[2]/ul/li[{page}]/*',
        )
        next_page_url = next_page_element.get_attribute("href")

        self.driver.get(str(next_page_url))
        logger.debug(page)
        logger.debug(type(page))
        # print(next_page_url)
        logger.info("navigating to next page")

        return next_page_url

    def get_information_from_page(self):

        page_information_dict = {}
        # TODO: This could be a staticmethod?
        for key, xpath in self.xpaths_dict.items():

            try:
                # if the key in the dictionary == description. Expand the description text on the page.
                if key == "Description":
                    # Look inside the container
                    web_element = self.driver.find_element(
                        By.XPATH, '//div[@class="summary_wrap"]'
                    )

                    try:
                        # try to find the collapse button inside the container using relative xpath './/'
                        collapse_button = web_element.find_element(
                            By.XPATH,
                            './/span[@class="toggle_expand_collapse toggle_expand"]',
                        )
                        if collapse_button:
                            collapse_button.click()
                            expanded_description = web_element.find_element(
                                By.XPATH, './/span[@class="blurb blurb_expanded"]'
                            )
                            page_information_dict[key] = expanded_description.text
                    # If there is no expand button inside the description field, set the key of information dict to the
                    # text of the xpath found.
                    except:
                        summary = web_element.find_element(By.XPATH, xpath)
                        page_information_dict[key] = summary.text

                else:
                    # Further logic for special cases: UUID and the Link_to_Page.
                    if key == "UUID":
                        page_information_dict[key] = str(uuid.uuid4())

                    elif key == "Link_to_Page":
                        web_element = self.driver.find_element(
                            By.XPATH, xpath
                        ).get_attribute("href")
                        page_information_dict[key] = web_element

                    else:
                        web_element = self.driver.find_element(By.XPATH, xpath)
                        page_information_dict[key] = web_element.text

            except:
                page_information_dict[key] = "Null"
                logger.warning("Null value recorded. Please check the xpath or webpage")

        logger.info("Dictionary Created")
        logger.info(page_information_dict)
        print(page_information_dict)
        return page_information_dict

    def process_page_links(self, file_name: str):

        list_of_all_pages_to_visit = []

        page_value = self.collect_number_of_pages(
            "#main_content > div.browse.new_releases > div.content_after_header > \
            div > div.next_to_side_col > div > div.marg_top1 > div > div > div.pages > ul > \
            li.page.last_page > a"
        )
        range_final = page_value + 1

        # Logic to remove the current text file if it exists already

        if os.path.exists(f"{file_name}.txt"):
            os.remove(f"{file_name}.txt")

        for i in range(1, range_final):
            with open(f"{file_name}.txt", "a+") as file:

                list_of_all_pages_to_visit.extend(
                    self.extract_page_links('//a[@class="title"]', "href")
                )
                while len(list_of_all_pages_to_visit) > 0:
                    url = list_of_all_pages_to_visit.pop(0)
                    file.write(str(url))
                    file.write("\n")
                try:
                    (
                        WebDriverWait(self.driver, 1).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    '//*[@id="main_content"]/div[1]/div[2]/div/div[1]/div/div[9]/div/div/div[1]/span[2]/a/span',
                                )
                            )
                        )
                    ).click()
                    logger.info("navigating to next page")
                except TimeoutException:
                    if range_final:
                        break
                # TODO: During this loop, the outputs of the links are stored inside a text file 
                # to be called when running the sample_scraper method

    def sample_scraper(self, file_name: str):
        # Goes to Games > Games Home > 'Search by Genre': Fighting > Scrapes 6 pages of content
        genre_list = self.choose_genre()
        self.driver.get(genre_list[2])

        self.process_page_links(file_name)

        with open(f"{file_name}.txt") as file:

            all_data_list = []

            for line in file:
                try:
                    self.driver.implicitly_wait(3)
                    self.driver.get(str(line))

                    all_data_list.append(self.get_information_from_page())

                except TimeoutException:
                    logger.warning("Timeoutexception on this page. Retrying.")
                    self.driver.implicitly_wait(3)
                    self.driver.refresh()

                    all_data_list.append(self.get_information_from_page())

            logger.info(all_data_list)
            self.save_json(all_data_list, "fighting-games")
            logger.info("Scrape complete! Exiting...")
            self.driver.quit()

        return all_data_list

    def create_dataframe(self, all_data_list):
        new_dataframe = DataCleaning(all_data_list, encoding="utf-8-sig")
        new_dataframe.clean_dataframe(all_data_list)


if __name__ == "__main__":
    new_scraper = MetaCriticScraper("https://www.metacritic.com")
