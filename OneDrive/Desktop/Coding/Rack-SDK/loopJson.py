import json 
json_file = open("articles.json")
dict_list = json.load(json_file)
fout = open("links.txt", 'w')
links = ""

for dicts in dict_list:
    links = links + (dicts.get("url") + "\n")

fout.write(links)