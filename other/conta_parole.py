#conta quanto frequentemente usi le 50 parole che usi più frequentemente in un testo
#non tiene conto delle maiuscole

import re 
from collections import Counter

def count_words(path):
    with open(path, encoding='utf-8') as file:
        all_words = re.findall(r"[0-9a-zA-Z-']+", file.read()) #cerca tutte le lettere e i numeri
        all_words = [word.upper() for word in all_words] #metti tutto in maiuscole
        print('\nTotal Words:', len(all_words))
     
    word_counts = Counter()
    for word in all_words:
        if len(word) > 4: #ragionevole che la somma di nome+cognome abbia più di 4 caratteri
            word_counts[word] += 1
    
    print('\nTop Words:')
    for word in word_counts.most_common(50): #qui scegli il numero di parole più frequenti che vuoi (50 attori in questo caso)
        print(word[0], '\t', word[1])