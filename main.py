### Importing packages ###
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
# drop warning
import warnings
warnings.filterwarnings('ignore')

#Importing dataset
def importing_film(fname):
    try:
        df = pd.read_excel(fname, skiprows=1) 
        return df
    except:
        print('Something not working in importing Excel File')

#Cleaning dataset    
def cleaning_df(df):
    #no space, but underscore
    for i in range(len(df.Titolo)):
        df.Titolo[i] = df.Titolo[i].replace(' ', '_')
    #removing the final underscore
    for i in range(len(df)):
        if df.Titolo[i][-1:] == '_':
            df.Titolo[i] = df.Titolo[i][:-1]
    return df

#Scraping genre and actors
def scraping(df, start, stop):
    lista = []
    for i in range(len(df)):
        url = "https://it.wikipedia.org/wiki/"+ df.Titolo[i] 
        #requests.get to retrieve the raw HTML content
        html_content = requests.get(url).text 
        #parses html content
        soup = BeautifulSoup(html_content, "lxml") 
        #transforms HTML content into string format
        text = soup.prettify()
        #from here onward it's a string
        try: 
            text = text.split(start)[1].split(stop)[0] 
        #if nothing is retrieved go on
        except:
            text = ' '
        #from string to list
        text = text.split('href') 
        #remove the first value that has nothing to do with it
        text = text[1:]
        #clean
        try: 
            for i in range(len(text)-1):
                #from title=" a " 
                text[i] = text[i].split('\n')[1].split('\n')[0] 
        except: 
            text = ' '
        #append values
        lista.append(text)
    return lista 
    
#scrape duration
def scraping_duration(df):
    '''
    it's easier than scraping because you have to extract
    a single value (a number) and not a list
    '''
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
    
#clean what we scraped
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
    
def cleaning_string_new(df_variable):
    '''
    Clean up the string data in the DataFrame variable.

    Args:
    df_variable (DataFrame): DataFrame containing string data to be cleaned.

    Returns:
    DataFrame: DataFrame with cleaned string data.
    '''
    for i in range(len(df_variable)):
        # Remove unwanted characters using regular expressions
        df_variable[i] = re.sub(r'[\[\].=/\'\"-]', '', str(df_variable[i]))
        # Remove extra spaces
        df_variable[i] = re.sub(r'\s+', ' ', df_variable[i])
        # Strip leading and trailing spaces
        df_variable[i] = df_variable[i].strip()
    return df_variable