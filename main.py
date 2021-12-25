#!/usr/bin/env python
# coding: utf-8

# In[34]:


import json
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# In[35]:


#Add command line argument of article url
parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("--url", help="loads the supplied url")
args = parser.parse_args()
#set selenium options to grab the page as quick as possible
_options = Options()
_options.page_load_strategy = 'none'
#initialize the driver
PATH = "/Users/weston/bin/chromedriver"
driver = webdriver.Chrome(PATH, options=_options)


# In[36]:


def write_article(url):
    try:
        driver.get(url)
    except InvalidArgumentException:
        print("invalid url supplied, program exiting")
        exit()
    print("got doc")
    with open("page_source.txt", "w") as f:
        #clear the file
        f.truncate(0)
        #write new source
        f.write(driver.page_source)
        driver.quit()


# In[27]:


def convert_to_html(file):
    with open(file, 'r') as NYTfile:
        text = NYTfile.read()
    #Actual article I usually read
    with open("page_source.html", "w") as HTMLfile:
        HTMLfile.truncate(0)
        HTMLfile.write(text)


# In[28]:


def get_json(file):
    with open(file, 'r') as NYTfile:
        source = NYTfile.read()
    #get the json they put on for quick loading
    start_index = source.find("window.__preloadedData")
    source = source[start_index:]
    end_index = source.find("\n")
    json = source[:end_index]
    json = json[25:]
    json = json[:-10]
    print("got json")
    #find whitespace and replace it with unique id
    json = json.replace(" ", "&%")
    with open("page.json", 'a') as JSONfile:
        JSONfile.truncate(0)
        JSONfile.write(json)


# In[29]:


#Returns objects at lowest level of the JSON
def filter_json(file):
    with open(file, 'r') as jsonFile:
        jsonDict = json.load(jsonFile)
    objectdict = getNestedVals(jsonDict)
    keysToDel = []
    for key in objectdict.keys():
        if "&%" not in objectdict[key]:
            keysToDel.append(key)
        else:
            objectdict[key] = objectdict[key].replace("&%", " ")
    for key in keysToDel:
        del objectdict[key]
    return objectdict


# In[30]:


#Depth first search of JSON
def getNestedVals(jsonDict, objectDict = {}):
    for key in jsonDict.keys():
        if isinstance(jsonDict[key], dict):
            objectDict = getNestedVals(jsonDict[key], objectDict)
        elif isinstance(jsonDict[key], list):
            for val in jsonDict[key]:
                if isinstance(val, str):
                    newKey = key
                    iterator = 0
                    while True:
                        iterator += 1
                        if not newKey in objectDict.keys():
                            objectDict[newKey] = jsonDict[key]
                            break
                        else:
                            newKey = str(key) + str(iterator) 
        else:
            if isinstance(jsonDict[key], str):
                newKey = key
                iterator = 0
                while True:
                    iterator += 1
                    if not newKey in objectDict.keys():
                        objectDict[newKey] = jsonDict[key]
                        break
                    else:
                        newKey = str(key) + str(iterator)
    return objectDict


# In[31]:


#Gets all elements with text attribute
def gen_body(jsonObjects):
    body = []
    for key in jsonObjects.keys():
        if "text" in key:
            body.append(jsonObjects[key])
    return body


# In[32]:


def gen_paragraphs(jsonObjects):
    body = gen_body(jsonObjects)
    paragraphs = []
    paragraph = ""
    iterator = 0
    for sentence in body:
        if len(paragraph) > 2000:
            paragraphs.append(paragraph)
            paragraph = ""
        else:
            paragraph = paragraph + sentence
    paragraphs.append(paragraph)
    return paragraphs


# In[33]:


if args.url is None:
    print("No url supplied, format is --url 'url_String'")
    exit()
write_article(args.url)
convert_to_html("page_source.txt")
driver.get("/page_source.html")
print("Is the full article present within the HTML? (Y/N)")
while true:
    answer = input()
    if answer == "N":
        break
    elif answer == "Y":
        exit()
get_json("page_source.txt")
#jsonObjects is a dict
jsonObjects = filter_json("page.json")
paragraphs = gen_paragraphs(jsonObjects)
print(paragraphs)


# In[ ]:




