from asyncore import write
from audioop import reverse
from copy import copy
from distutils.log import Log
from selenium import webdriver
from selenium.webdriver.common.by import By
from nltk.stem.snowball import SnowballStemmer
from selenium.webdriver.firefox.options import Options
import time

common_words = ("the", "a", "to", "of", "in", "and", "that", "for", "can", "they", "is", "this", "on", "are", "his", "them", "you", "our", "cookies", "buy", "subscribe")
def adddict(text, word_dict):
    text = text.rstrip(",.-\\")
    if len(text) < 4: 
        return word_dict

    if text == "":
        return word_dict

    if text in common_words:
        return word_dict

    if text in word_dict:
        count = word_dict.get(text)
        word_dict[text] +=1 
        return word_dict
    
    word_dict.update({text: 1})
    return word_dict

def main():
    fin = open("inputlinks.txt")
    lines = fin.readlines()
    head = Options()
    head.headless = True
    stemmer = SnowballStemmer("english")
    driver = webdriver.Firefox()
    file_num = 1

    for line in lines:
        word_dict = {}
        driver.get(line) 
        final_str = ""
        fout = open(f"output{file_num}.txt", "w", encoding="utf-8")
        words = driver.find_elements(By.TAG_NAME, 'p')
        for i in words:
            for s in i.text.split():
                adddict(stemmer.stem(s.lower().strip(",.() ")), word_dict)

        # Sort our dictionary
        new_dict = sorted(word_dict, key = word_dict.get, reverse=True)
        i = 0

        fout.write("")
        while i < len(new_dict):
            try: 
                final_str += (f"{new_dict[i]} {word_dict.get(new_dict[i])}\n") 
            except UnicodeEncodeError:
                i += 1
                continue
            i += 1
        
        file_num += 1
        time.sleep(2)
        fout.write(final_str)
        fout.close()

    fin.close()
    driver.close()

if __name__ == "__main__":
    main() 
