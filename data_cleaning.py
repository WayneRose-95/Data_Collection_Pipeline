import numpy as np 
import pandas as pd 
import os 

# Data Cleaning Plan 

'''
1. Read in the .json file 
2. Set the columns to the correct datatypes 
3. Use the correct string method for the titles
4. Clean the Date Field 

'''

class DataCleaning: 

    def __init__(self, file_pathway, encoding=None):
        self.data = self.create_dataframe(file_pathway) 

    
    def create_dataframe(self, file_pathway, encoding=None):
        raw_data = pd.read_json(file_pathway, encoding='utf-8-sig')
        return raw_data
    
    def clean_dataframe(self, file_pathway):
        # Create the dataframe 
        raw_data = self.create_dataframe(file_pathway)

        # Create a new column called 'id'
        raw_data['id'] = raw_data.index 

        # Set this column as the index of the dataframe 
        raw_data.set_index('id', inplace=True)

        # Convert the following columns into string datatypes 
        raw_data = raw_data.astype(
            {
            'Title': 'string', 
            'Link_to_Page': 'string', 
            'Platform': 'string',
            'Release_Date': 'string',
            'Developer': 'string',  
            'Description': 'string'}
        )
        
        # For all values inside the Title column, apply the string method .title() to capitalise every first letter. 
        raw_data.Title = raw_data.Title.str.title()

        # Change the column: Release_Date to a datetime object and change its formatting 
        raw_data['Release_Date'] = pd.to_datetime(raw_data['Release_Date'].astype(str), format='%b %d, %Y')
        raw_data['Release_Date'] = raw_data['Release_Date'].dt.strftime('%m/%d/%Y')

        # Next, change the columns: MetaCritic_Score and User_Score to an integer and a float respectively. 
        raw_data.MetaCritic_Score = pd.to_numeric(raw_data.MetaCritic_Score, errors='coerce').astype('Int64')
        raw_data.User_Score = pd.to_numeric(raw_data.User_Score, errors='coerce').astype('float64')

        # Lastly, for each column in the description column, strip the word 'Summary:' off of each of the records. 
        raw_data.Description = raw_data.Description.str.strip('Summary:')
        raw_data.head()
        
        # return the raw_data as a cleaned dataframe
        return raw_data

if __name__ == "__main__":
    file_path = os.getcwd()
    new_data = DataCleaning(file_path + '\\json-files\\fighting-games-details.json', encoding= 'utf-8-sig' )
    new_data.clean_dataframe(file_path + '\\json-files\\fighting-games-details.json')