### Importing packages ###
import pandas as pd
from bs4 import BeautifulSoup
import requests
# Non ci rompere il cazzo, grazie
import warnings
warnings.filterwarnings('ignore')

#Importing dataset
def importing_film(fname):
    try:
        df = pd.read_excel(fname, skiprows=1) 
        '''
        ritorna df! 
        importante perché le funzioni sotto dipendono da questa
        '''
        return df
    except:
        print('Porco Dio! Qualcosa non funziona qui!')

#Cleaning dataset    
def cleaning_df(df):
    '''
    df.drop(columns=['Id'], inplace=True)
    Se scrivessi:
    df = df.drop(columns=['Id'], inplace=True)
    cambierebbe il df-type da dataframe  a nonetype
    di conseguenza crasherebbe qui sotto
    (ora ho tolto sta colonna)
    '''
    #sostituisco lo spazio con l'underscore
    for i in range(len(df.Titolo)):
        df.Titolo[i] = df.Titolo[i].replace(' ', '_')
    #a volte ho l'underscore alla fine (perché prima avevo lo spazio), lo rimuovo 
    for i in range(len(df)):
        if df.Titolo[i][-1:] == '_':
            df.Titolo[i] = df.Titolo[i][:-1]
    return df

#Scrape genere e attori
def scraping(df, start, stop):
    '''
    start: gratta da ...
    stop: fino a...
    '''
    lista = []
    for i in range(len(df)):
        url = "https://it.wikipedia.org/wiki/"+ df.Titolo[i] 
        #requests.get per recuperare il contenuto HTML non elaborato
        html_content = requests.get(url).text 
        #analizza il contenuto html
        soup = BeautifulSoup(html_content, "lxml") 
        #trasforma il contenuto HTML in formato stringa
        text = soup.prettify()
        #da qui lo tratto come stringa
        try: 
            text = text.split(start)[1].split(stop)[0] 
        #se non trovi nulla lascia bianco e ciaone
        except:
            text = ' '
        #da stringa a lista
        text = text.split('href') 
        #togli il primo valore che non c'entra un cazzo
        text = text[1:]
        #pulisci
        try: 
            for i in range(len(text)-1):
                #da title=" a " 
                text[i] = text[i].split('\n')[1].split('\n')[0] 
        except: 
            text = ' '
        #appendi i valori
        lista.append(text)
    return lista 
    
#Grattare la durata del film
def scraping_duration(df):
    '''
    è più semplice di scraping perché devi estrarre 
    un solo valore (un numero) e non una lista
    '''
    lista = []
    for i in range(len(df)):
        url = "https://it.wikipedia.org/wiki/"+ df.Titolo[i]
        html_content = requests.get(url).text 
        soup = BeautifulSoup(html_content, "lxml") 
        text = soup.prettify()
        try:
            text = text.split('Durata')[1].split("min")[0]
            #estrai il numero all'interno della stringa
            text = [int(s) for s in text.split() if s.isdigit()] 
            #prima era lista, trasformalo in int
            text = text[0]
        except:
            text = ' '
        #appendi l'int che hai estratto sopra
        lista.append(text)
    return lista
    
#Puliamo ciò che abbiamo grattato da Wiki
def cleaning_string(df_variable):
    '''
    ripuliamo la maxi stringa di attori e generi
    
    inserisci quale variabile (attori o genere) del df vuoi pulire
    la durata è già a posto
    '''
    #segni che devono essere tolti (CAZZO, ESISTE UN METODO MIGLIORE, DATTI UNA SVEGLIA!)
    da_pulire = ["[", "]", ".", " ", "=", "/", "'", '"', '-']
    for i in range(len(df_variable)):
        for segni in da_pulire:
            df_variable[i] = str(df_variable[i]).replace(str(segni), "")
    
    
    