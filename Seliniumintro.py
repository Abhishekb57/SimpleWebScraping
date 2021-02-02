# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 11:11:23 2021

@author: abhis
"""


def findXpath(element,target,path):#this recursive function will find out path for target element
    
    if target in element.get_attribute("textContent") and element.tag_name=="script":
        return path
    newelements=element.find_elements_by_xpath("./*")
    for newelement in newelements:
        print(path+"/"+newelement.tag_name)
        final=findXpath(newelement,target,path+"/"+newelement.tag_name)
        if final!="":
            return final
    return ""

def findJsonpath(jsonobject,target,path,matchtype):
    if type(jsonobject)==matchtype:
        if target in jsonobject:
            return path
        for newkey in jsonobject:
            print(path)
            finalkey=findJsonpath(jsonobject[newkey],target,path +","+newkey,matchtype)
            if finalkey!="":
                return finalkey
    return ""
#selenium tutorial
from selenium import webdriver
import pandas as pd
import json
url="https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL"
options=webdriver.ChromeOptions()
options.add_argument('headless')

driver=webdriver.Chrome(executable_path="C:/Users/abhis/Webscraping/chromedriver_win32/chromedriver.exe",options=options)
driver.get(url)
#print(driver.page_source)
element=driver.find_element_by_xpath("html")#it will return element lists after html tag(* means go for everything after html)
#print("Final Path is",findXpath(element,"trailingPE","html"))#our aim to find out "trailingPE" in html text
#for element in elements:
#    newelements=element.find_elements_by_xpath("./*")
#    for newelement in newelements:
#        print(newelement.tag_name)
#    print(element.tag_name)
#print(element.get_attribute("textContent"))
FinalPath=findXpath(element,"trailingPE","html")
print("Final Path is",FinalPath)
elementcounters=driver.find_elements_by_xpath(FinalPath)
counter=1
for elementcounter in elementcounters:
    if "trailingPE" in elementcounter.get_attribute("textContent"):
        print(counter)
        break
    counter+=1
#newupdatedelement=driver.find_element_by_xpath(FinalPath+"["+str(counter)+"]")
newupdatedelement=driver.find_element_by_xpath(FinalPath+"["+str(counter)+"]")
tempdata=newupdatedelement.get_attribute("textContent").strip("(this));\n")
tempdata=tempdata.split("root.App.main = ")[1][:-3]
jsondata=json.loads(tempdata)
matchtype=type(jsondata)
print("Final Path for data is",findJsonpath(jsondata,"trailingPE","",matchtype))
finalData = jsondata["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["summaryDetail"]
df = pd.DataFrame(data = finalData)
print(df)
#print(jsondata.keys())
driver.quit()
