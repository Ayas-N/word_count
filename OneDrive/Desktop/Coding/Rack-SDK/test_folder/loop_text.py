from asyncore import write
from audioop import reverse
from copy import copy
from subprocess import call
import os
import nltk
from nltk import SnowballStemmer, WordNetLemmatizer
import spacy 
nltk.download('wordnet')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def add_dict(text, word_dict):
    anti_google = ("google", "article", "institute", "scholar")
    text = text.strip("()")
    text = text.strip("\"-,.\\")

    if text in anti_google:
        return word_dict

    if text in stop_words:
        return word_dict

    if text == "":
        return word_dict

    if len(text) < 4:
        return word_dict

    if text in word_dict:
        count = word_dict.get(text)
        word_dict[text] += 1 
        return word_dict
    
    word_dict.update({text: 1})
    return word_dict

def main(text):
    final_str = ""
    wnl = WordNetLemmatizer()
    stemmer = SnowballStemmer("english")
    word_dict = {}
    fin = open(f"outputs/{text}", encoding='utf-8')
    fout = open(f"dictOutputs/{text.rstrip('.txt')}_output.txt", "w", encoding='utf-8')
    text_words = fin.read().strip("\n (),.-")
    word_ls = text_words.split()

    for word in word_ls:
        if "references" in word:
            break
        e_check = wnl.lemmatize(word)
        if e_check.endswith('e'):
            word_dict = add_dict(wnl.lemmatize(word), word_dict)

        elif stemmer.stem(e_check) + "e" in word_dict:
            word_dict = add_dict(f"{stemmer.stem(e_check) + 'e'}", word_dict)

        elif e_check.endswith('r'):
            word_dict = add_dict(wnl.lemmatize(word), word_dict)
            
        elif stemmer.stem(e_check) + "r" in word_dict:
            word_dict = add_dict(f"{stemmer.stem(e_check) + 'r'}", word_dict)


    # Sort our dictionary
    new_dict = sorted(word_dict, key = word_dict.get, reverse=True)
    i = 0
    while i < len(new_dict):
        final_str += f"{new_dict[i]} {word_dict.get(new_dict[i])}\n"
        i += 1
    
    fout.write(final_str)
    
    fout.close() 


if __name__ == "__main__":
    contents = os.listdir("outputs")
    for txt_files in contents:
        main(txt_files)
    