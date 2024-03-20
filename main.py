### Importing packages ###
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import logging
import datetime as datetime
# drop warning
import warnings
warnings.filterwarnings('ignore')

# Logger Configuration
today_date = datetime.datetime.now().strftime(f'%Y-%m-%d')
log_filename = f'logs/log_{today_date}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Importing Excel file
def importing_film(fname):
    try:
        df = pd.read_excel(fname, skiprows=1)
        logging.info('Excel imported')
        return df
    except Exception as e:
        logging.error(f'Error importing Excel: {str(e)}')

# Cleaning Excel file    
def cleaning_df(df):
    try:
        #no space, but underscore
        for i in range(len(df.Titolo)):
            df.Titolo[i] = df.Titolo[i].replace(' ', '_')
        #removing the final underscore
        for i in range(len(df)):
            if df.Titolo[i][-1:] == '_':
                df.Titolo[i] = df.Titolo[i][:-1]
        logging.info('Excel file cleaned')
        return df
    except Exception as e:
        logging.error(f'Error cleaning Excel: {str(e)}')

# Scraping Genre and Actors
def scraping(df, start, stop):
    try:
        lista = []
        for i in range(len(df)):
            url = "https://it.wikipedia.org/wiki/"+ df.Titolo[i]        #requests.get to retrieve the raw HTML content
            html_content = requests.get(url).text                       #parses html content
            soup = BeautifulSoup(html_content, "lxml")                  #transforms HTML content into string format
            text = soup.prettify()                                      #from here onward it's a string
            try: 
                text = text.split(start)[1].split(stop)[0]              #if nothing is retrieved go on 
            except:
                text = ' '
            text = text.split('href')                                   #from string to list
            text = text[1:]                                             #remove the first value that has nothing to do with it
            try:                                                        #clean 
                for i in range(len(text)-1):
                    text[i] = text[i].split('\n')[1].split('\n')[0]     #from title=" a " 
            except: 
                text = ' '
            lista.append(text)                                          #append values
        return lista
    except Exception as e:
        logging.error(f'Error scraping genre and actors: {str(e)}')
      
# Scrape duration
def scraping_duration(df):
    '''
    it's easier than scraping because you have to extract
    a single value (a number) and not a list
    '''
    try:
        lista = []
        for i in range(len(df)):
            url = "https://it.wikipedia.org/wiki/"+ df.Titolo[i]
            html_content = requests.get(url).text 
            soup = BeautifulSoup(html_content, "lxml") 
            text = soup.prettify()
            try:
                text = text.split('Durata')[1].split("min")[0]
                #extract the number inside the string
                text = [int(s) for s in text.split() if s.isdigit()] 
                #before it was list, turn it into int
                text = text[0]
            except:
                text = ' '
            #append the int you extracted above
            lista.append(text)
        return lista
    except Exception as e:
        logging.error(f'Error scraping duration: {str(e)}')  
    
#clean what we scraped
def cleaning_string_new(df_variable):
    '''
    Clean up the string data in the DataFrame variable.

    Args:
    df_variable (DataFrame): DataFrame containing string data to be cleaned.

    Returns:
    DataFrame: DataFrame with cleaned string data.

    DIFFENT METHOD OF LOGGING, AFTER THE TRY/EXCEPT CLAUSE!
    '''
    for i in range(len(df_variable)):
        try:
            # Remove unwanted characters using regular expressions
            df_variable[i] = re.sub(r'[\[\].=/\'\"-]', '', str(df_variable[i]))
            # Remove extra spaces
            df_variable[i] = re.sub(r'\s+', ' ', df_variable[i])
            # Strip leading and trailing spaces
            df_variable[i] = df_variable[i].strip()
            # Log success message
            logging.info(f'Cleaned string data for index {i}')
        except Exception as e:
            logging.error(f'Error cleaning string data for index {i}: {str(e)}')
    return df_variable

def cleaning_string(df_variable):
    '''
    let's clean up the maxi string of actors and genres
    
     enter which variable (actors or genre) of the df you want to clean
     the duration is already in place   
    '''
    #signs that need to be removed (THERE IS A BETTER METHOD)
    da_pulire = ["[", "]", ".", " ", "=", "/", "'", '"', '-']
    for i in range(len(df_variable)):
        for segni in da_pulire:
            df_variable[i] = str(df_variable[i]).replace(str(segni), "")