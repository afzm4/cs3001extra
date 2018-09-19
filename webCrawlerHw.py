# -*- coding: utf-8 -*-
"""
Author: Andrew Floyd
Date: 9/19/2018
Course: CS 3001: Intro to Data Science
Bonus Homework
"""
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib, time, re
from random import random

def crawl(seeds, param=None):
    if param is None:
        param = 10
        
    frontier = seeds
    visited_urls = set()
    
    i = 0
    while i < param: 
        crawl_url = frontier.pop()
        print("Crawling:", crawl_url)
        i = i + 1
        visited_urls.add(crawl_url)
        
        try:
            resp = urllib.request.urlopen(crawl_url)
        except:
            print("Could not access ", crawl_url)
            continue
        
        content_type = resp.info().get('Content-Type')
        
        if not content_type.startswith('text/html'):
            print("Skipping %s content" % content_type)
            continue
    
        contents = str(resp.read())
        #print(contents)
        filename = 'pages/' + hashlib.md5(crawl_url.encode()).hexdigest()
        f = open("%s.html" % filename, 'w')
        f.write(contents)
        soup = BeautifulSoup(contents, "lxml")
        
        discovered_urls = set()
        links = soup('a')
        matchPer = re.compile('.*mst\.edu.*')
        for link in links:
            if ('href' in dict(link.attrs)):
                url = urljoin(crawl_url, link['href'])
                if matchPer.search(url):
                    if (url[0:4] == 'http' and url not in visited_urls
                        and url not in discovered_urls and url not in frontier):
                        discovered_urls.add(url)
                    
        frontier = frontier | discovered_urls
        time.sleep(random())

seeds = {"http://mst.edu"}
crawl(seeds)