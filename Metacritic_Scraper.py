import time
import os
import yaml 
from numpy import number
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from urllib3 import Timeout
from ScraperClass import Scraper
from data_cleaning import DataCleaning
from data_cleaning import DataCleaning
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd 

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
        with open('config/RDS_details_config.yaml') as file:
            creds = yaml.safe_load(file)
            DATABASE_TYPE = creds['DATABASE_TYPE']
            DBAPI = creds['DBAPI']
            ENDPOINT = creds['ENDPOINT']
            USER = creds['USER']
            PASSWORD = creds['PASSWORD']
            DATABASE = creds['DATABASE']
            PORT = creds['PORT']
        
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        self.engine.connect() 
        try:
            self.driver.set_page_load_timeout(30)
            self.land_first_page(url)
        except TimeoutException as ex:
            print("Exception has been thrown. " + str(ex))
            self.driver.quit()
        
        self.page_counter = 0
        
        # Dictionary of xpaths representing web_elements on the page. 
        self.xpaths_dict = {
            "uuid": "",
            "title": '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a/h1',
            "link_to_page": '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/a',
            "platform": '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[2]/span',
            "release_date": '//*[@id="main"]/div/div[1]/div[1]/div[1]/div[3]/ul/li[2]/span[2]',
            "metacritic_score": '//a[@class="metascore_anchor"]/div',
            "user_score": '//div[@class="userscore_wrap feature_userscore"]/a/div',
            "developer": '//li[@class="summary_detail developer"]/span[2]/a',
            "description": './/li[@class="summary_detail product_summary"]',
        }

        df = pd.read_sql("Fighting_Games", self.engine)
        self.href_list_scraped = list(df['link_to_page'])


    def accept_cookies(self, cookies_button_xpath: str):
        '''
        Method to click the accept cookies on the webpage 

        parameters: 
        cookies_button_xpath : str
        A string which represents the web element for the accept_cookies button 

        returns: 
        bool: True if the button exists 

        '''
        return super().accept_cookies(cookies_button_xpath)

    def choose_category(self, category_selection: str = "game" or "music"):

        """
        Method to choose a category on the webpage

        Parameters: 
        category_selection : str 
        A string representing the selection of the choice i.e. game or music

        returns: 
        category_selection : str 

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
        Method to choose the genre on the webpage

        Parameters: 
        None 

        Returns: 
        list_of_genre_links 

        Returns a list of links to the genres on the page. 

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


    def get_information_from_page(self):
        '''
        Method to collect the information from the webpage 

        Returns: 
        A dictionary containing key, value pairs for the information 
        extracted via the self.xpaths_dict. 
        '''
        page_information_dict = {}
        # Use tuple unpacking to iterate through the keys and values of the 
        # xpaths_dict 
        for key, xpath in self.xpaths_dict.items():

            try:
                # if the key in the dictionary == description. Expand the description text on the page.
                if key == "description":
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
                    if key == "uuid":
                        page_information_dict[key] = str(uuid.uuid4())

                    elif key == "link_to_page":
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

        '''
        Method to process the page links and store them inside a text_file

        Parameters: 
        file_name : str 

        The name of the file 

        Returns:
        None 
        '''
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
                # During this loop, the outputs of the links are stored inside a text file 
                # to be called when running the sample_scraper method

    def sample_scraper(self, file_name: str):

        '''
        A method which combines all of the previous methods to 
        scrape information from the webpage 

        Parameters: 
        file_name : str 
        The name of the file 
        '''
        # Goes to Games > Games Home > 'Search by Genre': Fighting > Scrapes 6 pages of content

        # Create a list of hrefs to scrape 
        genre_list = self.choose_genre()
        # Get the 2nd index of the genre_list i.e. Fighting Games in this case. 
        self.driver.get(genre_list[2])

        # Process the links and store them inside a .txt file to iterate through.
        self.process_page_links(file_name)

        # Open the file name and iterate through the links inside the file
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

        
    
    
    def record_check(self, table_name, column_name):
        '''
        Staticmethod to check if a record already exists inside the RDS. 

        How it will be checked: 
        Query the links to the pages of the website. 
        Store these inside a list 
        Everytime a page is loaded, check whether the link exists within the list. 
        If it does exist, skip scraping the page. 
        If it does not exist, scrape the page, and append it to the all_data_list. 
        
        '''

        
        # Inspect the engine of the RDS database. Find the table_name if it exists 
        if sqlalchemy.inspect(self.engine).has_table(table_name):
            
            # If it exists, run a query to select the specified column 
            sql = sqlalchemy.text(f'SELECT {column_name} FROM "{table_name}"')

            # Next, read the sql query into a pandas dataframe
            result = pd.read_sql_query(sql, self.engine)

            # Cast the pandas dataframe to a list to be compared. 
            href_list = result[column_name].tolist()
            print(href_list)
        # For each entry inside the list 
        # for entry in all_data_list:

        #     # convert it to a pandas dataframe 
        #     rds_entry = pd.DataFrame([entry])
        #     print(rds_entry)
        #     # If the entry is not in the list of items in the table name 

        #     if entry[column_name] in href_list:
        #         # Take the dataframe and append it to the RDS 
        #         logger.warning('This record already exists inside the database')

        #         return False
                
        #     # But if it does not exist, state that the record has already been scraped, then continue the process
        #     else:
        #         rds_entry.to_sql(table_name, self.engine, if_exists='append')
        #         return True
        # In either case, return the href_list to check against the href_list in the database
        return href_list

                       

if __name__ == "__main__":
    new_scraper = MetaCriticScraper("https://www.metacritic.com")
