import os
import pandas as pd
import numpy as np
import regex as re
from utils.scraping import Scrapper
from utils.munging import SoccerEventExtractor


dirname = os.path.dirname(__file__)
url_file = os.path.join(dirname, 'data/test_url.txt')

test_match_data = os.path.join(dirname, 'data/test_match.csv')

with open(url_file) as fp:
        url = fp.read()
        print(url)


match = "Man City vs Arsenal"
test_data = pd.read_csv(test_match_data)
n_rows,n_cols = test_data.shape
print(n_rows)
print(n_cols)

home_formation_test = "3-2-4-1"
away_formation_test = "4-3-3"

n_goals = 5
log = []
def test1():
    """
        Test to check number of rows and columns scraped by Scrapping 
    """
    scrape_object = Scrapper(url,match,log)
    df, _ = scrape_object.scrap()

    n_rows_check,n_cols_check = df.shape
    # Test 1: Check whether the scrpaed comments created by the classifier match what we expect
    assert np.allclose(np.array([n_rows_check,n_cols_check]), np.array([n_rows,n_cols]))

def test2():
    """
        Test to check if number of goals scroed is correctly pulled
    """
    scrape_object = Scrapper(url,match,log)
    df, _ = scrape_object.scrap()

    df = df[df['event'] == "goal"]
    
    r,c = df.shape
    n_rows_check = r
    # Test 2: Check whether the goals identified by the classifier match what we expect
    assert np.allclose(np.array([n_rows_check]), np.array([n_goals]))

    

def test3():
    """
        Test to check if formation extracted by regex is correct
    """
    scrape_object = Scrapper(url,match,log)
    df, _ = scrape_object.scrap()

    home_formation_check, away_formation_check = SoccerEventExtractor(df)._extract_formation(df)

    # Test 3: Check whether the formation identified by the classifier match what we expect
    assert away_formation_check , away_formation_test
    assert home_formation_check , home_formation_test









