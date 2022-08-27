from asyncore import write
from audioop import reverse
from copy import copy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from subprocess import call


common_words = ("the", "a", "to", "of", "in", "and", "that", "for", "can", "they", "is", "this", "on", "are", "his", "them", "you", "our", "cookies", "buy", "subscribe")

def main(link):
    link_ls = []
    final_str = ""
    driver = webdriver.Firefox()
    driver.get(link) 
    words = driver.find_elements(By.TAG_NAME, 'w')
    fout = open("output.txt", "a", encoding="ascii")
    
    for i in words:
        link_ls.append(i.get_attribute("href"))

    i = 0
    top_five = []
    while i < len(link_ls):
        try: 
            final_str += (f"{link_ls[i]}")
        except UnicodeEncodeError:
            i += 1
            continue
        i += 1
    
    fout.write(final_str)
    fout.close() 

    assert "No results found." not in driver.page_source
    driver.close()

if __name__ == "__main__":
    # fin = open("inputlinks.txt")
    # lines = fin.readlines()
    # for line in lines:
    #     main(line)
    main("https://www.science.org/action/doSearch?%00=&startPage=1&rel=nofollow&ConceptID=505155&pageSize=100&adobe_mc=MCMID%3D75405697622458117371353586827930229093%7CMCORGID%3D242B6472541199F70A4C98A6%2540AdobeOrg%7CTS%3D1661573233")