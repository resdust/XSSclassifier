#!/usr/bin/python3
# -*- encoding:utf-8 -*-

import re, csv, time, socket
import pandas as pd
import urllib.error as error
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup

#open file and load data(websites with XSSed tags) to returned value
def opendata(path):
    df = pd.read_csv(path)
    list_label = df.columns.values 
    list_data =df.values.tolist()
    print("These columns have been read:",list_label) #print columns header
    return list_data

#extract relative urls from website
def extract(url):
    meg = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'} #fake header
    r = urllib.request.Request(url,headers=meg) 
    fp = urllib.request.urlopen(r) #send request and open url   
    s = fp.read()
    soup = BeautifulSoup(s,features="html.parser")
    alist = soup.find_all('a') #all the 'a' tags
    fp.close()
    urlDct = {} #extracted urls as key while occurence number as value
    for tag in alist:
        href = tag.get('href')
        if href != None:
            if(href in urlDct):
                urlDct[href] += 1
            else:
                urlDct[href] = 1
    return urlDct

#extract features from urls in unique website
def URLfeature(suburl):
    if(suburl==None):
        return (['Failed to open the website!','' ,'' ,'' ])
    longUrlCount = maxUrlSize = xssCount = obfuscatedCharCount = 0
    XSS = [r"<scrip",r"</script",r"<iframe",r"</ifirame",r"response_write(",r"eval(",r"prompt(",r"alert(",r"javascript:",r"document.cookie"]
    first = 0
    for d in suburl:
        size = len(d)
        #The maximum size of URLs
        if (first == 0):
            first = 1
            maxUrlSize = size
        else:
            maxUrlSize = (size > maxUrlSize) and size or maxUrlSize
        
        #Total count of URLs with high level malicious XSS keywords
        for key in XSS:
            if (d.find(key) != -1):
                xssCount += 1
                break

        #Total count of long URLs
        if len(d) > 120:
            longUrlCount += 1
       
        #Total count of URLs with maximum number of obfuscated characters
        special = re.split(r'%', d)
        if (len(special)-1) > (len(d)/3):
            obfuscatedCharCount += 1
    return [longUrlCount, maxUrlSize, xssCount, obfuscatedCharCount]

#write analysed result to a new csv file
def loadData(website, xss, data):
    with open("Features.csv","a",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([website, xss, data[0], data[1], data[2], data[3]])
       
def start():
    stime = time.process_time()
    socket.setdefaulttimeout(20)
    try:
        with open("Features.csv","w+",newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Website','XSSed', 'longUrlCount', 'maxUrlSize', 'xssCount', 'obfuscatedCharCount'])   
    except PermissionError as e:
        print("Failed to open file! Please close your \'Features.csv\' file.")
        exit(0)
    path = r'.\XSSArchive3.csv'
    LIST = opendata(path) #read data
    limit = 0
    for url in LIST:
        limit += 1
        try:
            subUrl = extract('http://'+url[0]) 
        except error.URLError as e:
            subUrl = None
            print("Unable to open:", url[0])
            print(e.reason)
        except WindowsError as e:
            subUrl = None
            print("Unable to open:", url[0])
            print(e)
        else:
            ttime = time.process_time()
            print("Loading website", limit, "...", url[0], "...at time:", ttime-stime)
        time.sleep(10)
        features = URLfeature(subUrl)
        xss = (url[1]=='R') and 1 or 0 #1 for XSSed and 0 for non-XSSed
        loadData(url[0], xss, features)
        if(limit >= 10):
            break
    print("END")

start()