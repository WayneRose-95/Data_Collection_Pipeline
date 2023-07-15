
import numpy as np 
import pandas as pd 
import os 
import yaml
from file_handler import get_absolute_file_path
from sqlalchemy import create_engine, VARCHAR, TIMESTAMP, INTEGER, BOOLEAN, FLOAT, DATE
from sqlalchemy.dialects.postgresql import UUID
from database_connection import DatabaseConnector


class DatabaseCleaner(DatabaseConnector):
    def __init__(self, config_file : yaml, database_name : str):
        # Inherit the methods from the DatabaseConnector class 
        super().__init__()
        connection_string = self.create_connection_string(config_file, True, database_name)

        self.engine = create_engine(
            connection_string
            )
        self.engine.connect() 

    def source_data_to_dataframe(self, file_pathway, encoding='utf-8-sig'):
       
        try:
            dataframe = pd.read_json(file_pathway, encoding=encoding)
            return dataframe 

        except ValueError:
            print("Please check file pathway")

    def land_games_data(self, games_df : pd.DataFrame):

        # Stripping off the first characters of the strings using regex patterns 
        games_df['description'] = games_df['description'].str.replace(r'^(Summary):\s', '', regex=True)
        games_df['genre'] = games_df['genre'].str.replace(r'^Genre\(s\):\s', '', regex=True)
        games_df['rating'] = games_df['rating'].str.replace(r'^(Rating):\s', '', regex=True)

        # Replacing 'Null' or 'No Details' with np.nan values 

        games_df["developer"] = games_df["developer"].replace('No Details', np.nan)
        games_df["developer"] = games_df["developer"].replace('No Details', np.nan)
        games_df["metacritic_score"] = games_df["metacritic_score"].replace('tbd', np.nan)
        games_df["user_score"] = games_df["user_score"].replace('tbd', np.nan)
        games_df["number_of_players"] = games_df["number_of_players"].replace("No Details", np.nan)
        games_df["number_of_players"] = games_df["number_of_players"].replace("On GameFAQs", np.nan).replace('', np.nan)

        games_df["release_date"] = pd.to_datetime(games_df["release_date"])

        # ========= COLUMN ADDITIONS  =======================

        # Adding online_flag column to disinguish between online games 
        games_df['online_flag'] = games_df['number_of_players'].str.contains('Online', na=False)

        # Set 'online_flag' to False for 'No Online Multiplayer'
        games_df.loc[games_df['number_of_players'] == 'No Online Multiplayer', 'online_flag'] = False
        
        # Creating '2D_flag' column if the genre column for the record has '2D' in it 
        games_df['2D_flag'] = games_df['genre'].str.contains('2D')

        # Create '3D Flag' column
        games_df['3D_flag'] = games_df['genre'].str.contains('3D')

        return games_df

    def upload_to_database(
            self, 
            dataframe : pd.DataFrame, 
            datastore_table_name : str, 
            connection, 
            column_datatypes,
            table_condition="replace"
            ):
        
        try:
            dataframe.to_sql(
                datastore_table_name, 
                con=connection, 
                if_exists=table_condition, 
                dtype=column_datatypes
                )
            print(f"{datastore_table_name} uploaded to database")
        except:
            print("Error uploading table to the database")
            raise Exception

if __name__ == "__main__":
    # Get the file pathway for the .json file 
    json_file_pathway = get_absolute_file_path("fighting-games-details.json", "json-files")
    config_file_path = get_absolute_file_path("rds_details_local_config.yaml", "config")
    # Instantiate an instance of the DatabaseCleaner class 
    cleaner = DatabaseCleaner(config_file_path, 'metacritic_database')
    # Read the table into a dataframe 
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






