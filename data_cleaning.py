import numpy as np 
import pandas as pd 
import os 
from sqlalchemy import create_engine
import yaml 

# Data Cleaning Plan 

'''
1. Read in the .json file 
2. Set the columns to the correct datatypes 
3. Use the correct string method for the titles
4. Clean the Date Field 

'''

class DataCleaning: 

    '''
    A class which contains methods which extracts .json files. 
    Files are converted into a Pandas dataframe, from which they are cleaned.
    Cleaned dataframes are then uploaded to the RDS given in the config file. 

    Attributes:
    self.engine: The connection to the RDS configured via the config file. 

    '''

    def __init__(self): 
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
    
    def create_dataframe(self, file_pathway : str, encoding=None):
        '''
        Method to create a dataframe and return the data as a dataframe 

        Parameters: 
        file_pathway:
        The path to your .json file 

        encoding=None:
        An optional argument for reading irregular characters. 

        Returns: 
        raw_data: 
        The dataframe which has been converted from the .json file. 
        '''
        raw_data = pd.read_json(file_pathway, encoding='utf-8-sig')
        return raw_data
    
    def clean_dataframe(self, file_pathway : str, table_name : str):
        '''
        Method to clean the dataframe using pandas functions 

        Parameters: 
        file_pathway:
        The path to your .json file 

        table_name: 
        The name of the table that the user can choose for the RDS. 
        '''
        # Create the dataframe 
        raw_data = self.create_dataframe(file_pathway)

        # Create a new column called 'id'
        raw_data['id'] = raw_data.index 

        # Set this column as the index of the dataframe 
        raw_data.set_index('id', inplace=True)

        # Convert the following columns into string datatypes 
        raw_data = raw_data.astype(
            {
            'title': 'string', 
            'link_to_page': 'string', 
            'platform': 'string',
            'release_date': 'string',
            'developer': 'string',  
            'description': 'string'}
        )
        
        # For all values inside the title column, apply the string method .title() to capitalise every first letter. 
        raw_data.title = raw_data.title.str.title()

        # Change the column: release_date to a datetime object and change its formatting 
        raw_data['release_date'] = pd.to_datetime(raw_data['release_date'].astype(str), format='%b %d, %Y')
        raw_data['release_date'] = raw_data['release_date'].dt.strftime('%m/%d/%Y')

        # Next, change the columns: metacritic_score and user_score to an integer and a float respectively. 
        raw_data.metacritic_score = pd.to_numeric(raw_data.metacritic_score, errors='coerce').astype('Int64')
        raw_data.user_score = pd.to_numeric(raw_data.user_score, errors='coerce').astype('float64')

        # Lastly, for each column in the description column, strip the word 'Summary:' off of each of the records. 
        raw_data.description = raw_data.description.str.strip('Summary:')
        raw_data.head()
        # Send the data to the RDS. If the table already exists, replace it. 
        raw_data.to_sql(table_name, con=self.engine, if_exists='replace')
        # return the raw_data as a cleaned dataframe
        return raw_data

if __name__ == "__main__":
    file_path = os.getcwd()
    new_data = DataCleaning()
    new_data.clean_dataframe(file_path + '\\json-files\\fighting-games-details.json', 'Fighting_Games')