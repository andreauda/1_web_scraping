from main import *

fname = "film_input.xlsx"

df = importing_film(fname)
df = cleaning_df(df)
df.head()

#estrai attori
start_attori = 'wiki/Personaggio_immaginario'
stop_attori = '</table>'
attori = scraping(df, start_attori, stop_attori)
#estrai generi
start_generi = 'wiki/Genere_cinematografico'
stop_generi = 'wiki/Regia_cinematografica'
generi = scraping(df, start_generi, stop_generi)
#estrai durata
durata = scraping_duration(df)

#a volte tira fuori roba senza capo nè coda (forse lo fa con alcuni film italiani)
for element in attori, generi: 
    if len(element) > 50:
        element = ''
        
#passo ciò che ho estratto, al dataframe
df['generi'] = generi
df['attori'] = attori
df['durata'] = durata

#puliamo un po' di schifezze che abbiamo raccolto (virgolette, puntini, cazzini ecc.)
cleaning_string(df.attori)
cleaning_string(df.generi)

#salvo il file Excel con la maxi stringa unica (qui potrai cercare tutti gli attori caro il mio professorune sapientune)
output_directory = 'C://Users//Utente//Dropbox//Culture//Film//'
output_filename = 'film_output.xlsx'
#salvo il dataframe
df.to_excel(output_directory+output_filename, index=False)

#riapro il dataframe
output_filename = "film_output.xlsx"
df =  pd.read_excel(output_filename)

#creo un dataframe provvisiorio, dove ogni colonna corrisponde ad un attore separato 
df_attori = df.attori.str.split(",", expand=True,)
testo_attori = pd.DataFrame() #creo un dataset vuoto (questo sarà il "definitivo")
for i in range(8):  #qui seleziono il numero di attori che voglio (prendo i primi 6/8) 
    testo_attori['attore'+str(i+1)] = df_attori[i] #rinomino le colonne del dataset "definitivo"
    
#faccio la stessa cosa per i generi
df_genere = df.generi.str.split(",", expand=True,)
testo_generi = pd.DataFrame()
for i in range(5):  
    testo_generi['genere'+str(i+1)] = df_genere[i]

#questo è il dataframe "definitivo" con il numero di attori pari al numero che ho scelto (continua sotto)
testo_attori

#lo salvo come .txt, mi servirà per contare le parole (e dunque gli attori) più frequenti
directory_output_txt = r'C://Users//Utente//Dropbox//Culture//Film//other//txt_output//'
testo_attori.to_csv(directory_output_txt+'testoattori.txt', header=None, index=None, sep=',')
testo_generi.to_csv(directory_output_txt+'testogenere.txt', header=None, index=None, sep=',')

#ora devo togliere gli accenti dai due .txt che mi sono creato, usando il pacchetto apposito
from unicodedata import category, normalize

#apro i due .txt
directory_output = 'C://Users//Utente//Dropbox//Culture//Film//other//txt_output//'
attori = open(directory_output+'testoattori.txt', 'r', encoding="utf8").read() 
generi = open(directory_output+'testogenere.txt', 'r', encoding="utf8").read()
#sostituisco tutti gli accenti strani con dei caratteri standard senza accenti
Attori = ''.join(c for c in normalize('NFD', attori) if category(c) != 'Mn')
Generi = ''.join(c for c in normalize('NFD', generi) if category(c) != 'Mn')

#creo due nuovi file .txt senza accenti 
attori_file = open(directory_output+"testoattori_senzaaccenti.txt", "w", encoding="utf8") #"w" sta per write
generi_file = open(directory_output+"testogeneri_senzaaccenti.txt", "w", encoding="utf8") #"w" sta per write

#e ci scrivo dentro la stringa senza accenti
n1 = attori_file.write(Attori)
n2 = generi_file.write(Generi)
#chiudo
attori_file.close()
generi_file.close()

### contiamo il numero di attori ###
directory_output = 'C://Users//Utente//Dropbox//Culture//Film//other//txt_output//'
from other.conta_parole import count_words
count_words(directory_output+'testoattori_senzaaccenti.txt')