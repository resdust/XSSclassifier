#!python3
# -*- encoding:utf-8 -*-

import re
import pandas as pd
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def opendata(path):
    df = pd.read_csv(path)
    list_label = df.columns.values 
    list_data =df.values.tolist()
    print(list_label)
    return list_data

def extract(url):
    meg = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    r = urllib.request.Request(url,headers=meg)
    fp = urllib.request.urlopen(r)
    s = fp.read()
    soup = BeautifulSoup(s,features="html.parser")
    polist = soup.find_all('a')
    urlDct = {}
    for tag in polist:
        href = tag.get('href')
        if href != None:
            if(href in urlDct):
                urlDct[href] += 1
            else:
                urlDct[href] = 1
    return urlDct

def URLfeature(dct):
    #domains = []
    longUrlCount = maxUrlSize = maxOcurDomain = obfuscatedCharCount = 0
    for d in dct:
        if len(d) > 120:
            longUrlCount += 1
    print('longUrlCount=',longUrlCount)

def domain(url):
    res = urlparse(url).netloc
    print(res)
    return res

url1 = 'https://www.jianshu.com/p/1476a181fc57'

def start():
    path = r'.\XSSArchive3.csv'
    LIST = opendata(path)
    limit = 0
    for url in LIST:
        url[1] = (url[1]=='R') and 1 or 0
        subUrl = extract('http://'+url[0])
        URLfeature(subUrl)
        limit += 1
        if(limit >= 1):
            break

subUrl = extract(url1)
URLfeature(subUrl)