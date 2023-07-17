from Metacritic_Scraper import MetaCriticScraper
from data_cleaning import DatabaseCleaner
from file_handler import get_absolute_file_path
from sqlalchemy import  VARCHAR, INTEGER, BOOLEAN, FLOAT, DATE
from sqlalchemy.dialects.postgresql import UUID
from time import time 
from datetime import datetime 
import logging
import os


log_filename = "logs/main.log"
if not os.path.exists(log_filename):
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)

main_logger = logging.getLogger(__name__)

# Set the default level as DEBUG
main_logger.setLevel(logging.DEBUG)

# Format the logs by time, filename, function_name, level_name and the message
format = logging.Formatter(
    "%(asctime)s:%(filename)s:%(funcName)s:%(levelname)s:%(message)s"
)
file_handler = logging.FileHandler(log_filename)

# Set the formatter to the variable format

file_handler.setFormatter(format)

main_logger.addHandler(file_handler)

main_logger.info(f"Beginning process at {datetime.now()}")

############# FILE PATHWAYS ######################
main_logger.info(f"Searching for file pathways to configuration and source data")

configuration_file_path = get_absolute_file_path("rds_details_local_config.yaml", "config")


main_logger.info(f"Path to configuration file {configuration_file_path}")


start_time = time()

############ MODULE INSTANCES ####################
cleaner = DatabaseCleaner(
    configuration_file_path, 
    "metacritic_database"
    )
new_scraper = MetaCriticScraper("https://www.metacritic.com")

############# EXTRACTING DATA FROM WEBSITE ##########
main_logger.info("Beginning Source Data Extraction")
new_scraper.accept_cookies('//button[@id="onetrust-accept-btn-handler"]')
new_scraper.choose_category("game")
new_scraper.scrape_details(
    "list_of_fighting_links", 
    "fighting-games" 
    )
main_logger.info("Beginning Source Data Extraction")


########## DATA CLEAING PROCESS TO CLEAN DATAFRAME ##############
json_file_pathway = get_absolute_file_path("fighting-games-details.json", "json-files")
main_logger.info(f"Path to source data: {json_file_pathway}")

raw_dataframe = cleaner.source_data_to_dataframe(json_file_pathway)

datastore_table = cleaner.land_games_data(raw_dataframe)
# Use the dataframe to upload to the datastore under the title "land_fighting_games_data"
cleaner.upload_to_database(
    dataframe=datastore_table, 
    datastore_table_name="land_fighting_games_data", 
    connection=cleaner.engine, 
    column_datatypes= {
                        "uuid": UUID,
                        "title": VARCHAR(255),
                        "link_to_page": VARCHAR(255),
                        "platform": VARCHAR(100),
                        "release_date": DATE,
                        "metacritic_score": INTEGER,
                        "user_score": FLOAT,
                        "developer": VARCHAR(255),
                        "publisher": VARCHAR(255),
                        "number_of_players": VARCHAR(50),
                        "rating": VARCHAR(10),
                        "genre": VARCHAR(255),
                        "description": VARCHAR(8000),
                        "online_flag": BOOLEAN,
                        "2D_flag": BOOLEAN,
                        "3D_flag": BOOLEAN
                    },
        )

end_time = time() 

time_elapsed = end_time - start_time

print(f"Time elapsed: {time_elapsed}")
main_logger.info(f"Time elapsed: {time_elapsed}")
