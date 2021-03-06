from Metacritic_Scraper import MetaCriticScraper
from data_cleaning import DataCleaning
import logging
import os

log_filename = "logs/main.log"
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

file_path = os.getcwd()

    
new_scraper = MetaCriticScraper("https://www.metacritic.com")
new_scraper.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
new_scraper.choose_category("game")
new_scraper.scrape_details(
    "list_of_fighting_links", 
    "fighting-games",
    file_path + '\\json-files\\fighting-games-details.json', 
    'Fighting_Games' 
    )

# TODO: find a way to make both classes interact with each other within this file.
# Temporary Solution: Move the methods from data_cleaning.py into Metacritic_Scraper.py 
# Potential Improvement for TODO still applicable. 
