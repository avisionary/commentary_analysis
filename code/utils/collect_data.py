# importing modules
from requests import get
from bs4 import BeautifulSoup
import datetime
import regex as re
import pandas as pd
from unidecode import unidecode
from code.utils.scraping import Scrapper

class MulitScraping():
    """
        Class to scrape multiple links using the Scrapper class
    """
    def __init__(self,links_path,output_path):
        """
            Constructor method to initialize class instance variables.
        """
        self.links_path = links_path
        self.commentory_df = pd.DataFrame(columns=['time', 'comment', 'event', 'event_player', 'event_team',
       'comment_desc', 'home_team', 'home_team_abbr', 'away_team',
       'away_team_abbr', 'full_time_score', 'match', 'date', 'link'])
        self.output_path = output_path

    def __str__(self):
        """
            Returns a string representation of the object.
        """
        return f"Scraping all match links from {self.links_path}"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({str(self)})>"
    
    def get_data(self):
        """
            Method to scrape data from the given match links and store in a dataframe.
        """
        counter = 0 # initialize counter to keep track of number of matches scraped

        for idx,row in self.links_path.iterrows():
            match = row['match'] # get the name of the match
            url = row['live_ticker'] # get the link to the match live ticker

            # scrape the data using the Scrapper class
            temp = Scrapper.scrap(url,match,Scrapper.log)

            if temp[1] == 1:
                counter += 1 # increment counter
                temp_df = temp[0] # get the dataframe containing scraped data
                temp_df['match'] = match # add the match name as a new column
                temp_df['date'] = row['match_day'] # add the match date as a new column
                temp_df['link'] = row['live_ticker'] # add the match link as a new column

                # concatenate the dataframes
                self.commentory_df = pd.concat([self.commentory_df,temp_df])

        # Check number of links scraped
        print("Total matches scraped : {counter}")

        # check logs
        self.__check_logs

        #save data in output file
        self.__save_data(self.commentory_df)

        # return df just in case
        return self.commentory_df

    def __check_logs(self):
        """
            Method to print the logs generated during scraping.
        """
        print(Scrapper.log)


    def __save_data(self,data):
        """
            Method to save the scraped data to a CSV file.
        """
        data.to_csv(self.output_path,index=False) 


                