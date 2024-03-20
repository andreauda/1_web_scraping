from main import *

fname = "film_input.xlsx"

df = importing_film(fname)
df = cleaning_df(df)
df.head()

#actors
start_attori = 'wiki/Personaggio_immaginario'
stop_attori = '</table>'
attori = scraping(df, start_attori, stop_attori)
#genres 
start_generi = 'wiki/Genere_cinematografico'
stop_generi = 'wiki/Regia_cinematografica'
generi = scraping(df, start_generi, stop_generi)
#duration
durata = scraping_duration(df)

#sometimes the extraction is not good, better to delete
for element in attori, generi: 
    if len(element) > 50:
        element = ''
        
#what I extracted to the dataframe
df['generi'] = generi
df['attori'] = attori
df['durata'] = durata

#cleaning
cleaning_string(df.attori)
cleaning_string(df.generi)

#saving temporary dataframe
output_directory = 'C://Users//Utente//Dropbox//Culture//Film//'
output_filename = 'film_output.xlsx'
#saving dataframe
df.to_excel(output_directory+output_filename, index=False)

#reopening dataframe
output_filename = "film_output.xlsx"
df =  pd.read_excel(output_filename)

#temp dataframe, where each column is a different actor
df_attori = df.attori.str.split(",", expand=True,)
testo_attori = pd.DataFrame()                               #empty dataset (the last one)
for i in range(8):                                          #select max number of actors (8 in this case)
    testo_attori['attore'+str(i+1)] = df_attori[i]          #renaming columns
    
#same for genres
df_genere = df.generi.str.split(",", expand=True,)
testo_generi = pd.DataFrame()
for i in range(5):  
    testo_generi['genere'+str(i+1)] = df_genere[i]

#final dataframe, with the number of actors equal to 8 
testo_attori

#I save the .txt, I'll use it to count the actors 
directory_output_txt = r'C://Users//Utente//Dropbox//Culture//Film//other//txt_output//'
testo_attori.to_csv(directory_output_txt+'testoattori.txt', header=None, index=None, sep=',')
testo_generi.to_csv(directory_output_txt+'testogenere.txt', header=None, index=None, sep=',')

#removing accents with the specific packages
from unicodedata import category, normalize

#open the two .txt files
directory_output = 'C://Users//Utente//Dropbox//Culture//Film//other//txt_output//'
attori = open(directory_output+'testoattori.txt', 'r', encoding="utf8").read() 
generi = open(directory_output+'testogenere.txt', 'r', encoding="utf8").read()
#I replace all the strange accents with standard characters without accents
Attori = ''.join(c for c in normalize('NFD', attori) if category(c) != 'Mn')
Generi = ''.join(c for c in normalize('NFD', generi) if category(c) != 'Mn')

#I create two new .txt files without accents
attori_file = open(directory_output+"testoattori_senzaaccenti.txt", "w", encoding="utf8") #"w" sta per write
generi_file = open(directory_output+"testogeneri_senzaaccenti.txt", "w", encoding="utf8") #"w" sta per write

#and I write the string without accents inside
n1 = attori_file.write(Attori)
n2 = generi_file.write(Generi)
#close
attori_file.close()
generi_file.close()

### contiamo il numero di attori ###
directory_output = 'C://Users//Utente//Dropbox//Culture//Film//other//txt_output//'
from conta_parole import count_words
count_words(directory_output+'testoattori_senzaaccenti.txt')