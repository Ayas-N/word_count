from asyncore import write
from audioop import reverse
from copy import copy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

word_dict = {}
common_words = ("the", "a", "to", "of", "in", "and", "that", "for", "can", "they", "is", "this", "on", "are", "his", "them")
def adddict(text):
    if text == "":
        return 

    if text in common_words:
        return

    if text in word_dict:
        count = word_dict.get(text)
        word_dict[text] +=1 
        return
    
    word_dict.update({text: 1})
    return 

def main():
    fin = open("links.txt")
    driver = webdriver.Firefox()
    driver.get("https://www.nature.com/articles/d41586-022-02334-2")    
    words = driver.find_elements(By.TAG_NAME, 'p')
    fout = open("output.txt", "w")
    
    for i in words:
        for s in i.text.split():
            (adddict(s.lower()))

    # Sort our dictionary
    new_dict = sorted(word_dict, key = word_dict.get, reverse=True)
    i = 0
    top_five = []
    while i < 5:
        write(f"{new_dict[i]} {word_dict.get(new_dict[i])}\n") 
        i += 1
    
    
    fout.close() 

    assert "No results found." not in driver.page_source
    driver.close()

if __name__ == "__main__":
    main()