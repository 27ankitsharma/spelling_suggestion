##------------- Author: Ankit Sharma, email: 27ankitsharma@gmail.com -------------##

import re
from collections import Counter


## ---------- Handling combined words. This will use spell correction part defined below---------##	
def spell_suggestion(input_string):
    if (input_string.strip() is ""):  # handling blank or all whitespace characters input
        print ("Please enter a valid string..!")
        return
    		
    input_string = re.sub('[^A-Za-z]+', '', input_string).lower()  # Keeping only the characters not the numbers.
	
    if (input_string in WORDS) or  (len(input_string) < 4): # assuming merged words are longer than 3 characters.
        final_suggestions = candidates(input_string)
    
    else:
        both_exist_list = []
        single_exist_list = []
        
        for i in range(1, len(input_string)-2):  # splitting input string into two words
            w1 = input_string[0:i+1]
            w2 = input_string[i+1:len(input_string)]
            
            if (w1 in WORDS and w2 in WORDS): # both the words are present in the dictionary
                both_exist_list.append([w1 + ' ' +w2]) 
            
            elif (w1 in WORDS and w2 not in candidates(w2)): # when only single word is present in the dictionary   
                print (w1, "exists in dictionary")
                single_exist_list.append([w1 + ' ' + x for x in candidates(w2)]) 
                
            elif (w2 in WORDS and w1 not in candidates(w1)): # when only single word is present in the dictionary
                print (w2, "exists in dictionary")
                single_exist_list.append([x + ' ' + w2 for x in candidates(w1)]) 
                
        
        # Flattening the lists
        both_exist_list   = [item for sublist in both_exist_list for item in sublist]
        single_exist_list = [item for sublist in single_exist_list for item in sublist]
        final_suggestions = list(set(candidates(input_string) + both_exist_list + single_exist_list))
        
        if len(final_suggestions)==0 : # if both lists are empty
            final_suggestions = candidates(input_string)
                            
    return final_suggestions
	
	
	
	
	
## -------------------- Spelling correction part ----------------------------##	

def words(text): 
    "Splitting string text into words and lowercasing all the words."
    return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('words_corpus.txt').read()))   # creating dictionary from the corpus


def P(word, N=sum(WORDS.values())): 
    "Probability of `word`. This is not being used currently but I thought of using it to improve the ranking of the returned results"
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return list(set(w for w in words if w in WORDS))

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))