import requests
from bs4 import BeautifulSoup
import pymongo
import re

client = pymongo.MongoClient('localhost',27017)
BaiduYun = client['BaiduYun']
threads = BaiduYun['threads']
groups = BaiduYun['groups']
url = 'http://www.baiduyuns.com/forum-36-1.html'

def get_threads(url):
    s = requests.get(url)
    soup = BeautifulSoup(s.text,'lxml')
    links = soup.find_all('a','s xst')[5:]
    links_in_db = [item['url'] for item in threads.find()]
    new_links=[]
    for link in links:
        new_links.append(link.get('href'))
    x = set(links_in_db)
    y = set(new_links)
    links_we_need = y - x
    for link in links_we_need:
        data = {
            'url':link,
        }
        threads.insert_one(data)
        print(data)

def get_group_links(url):
    s = requests.get(url)
    soup = BeautifulSoup(s.text, 'lxml')
    links = soup.find_all('td', 't_f')
    links_in_db = [item['url'] for item in groups.find()]
    x = set(links_in_db)
    pattern = re.compile('http(?:s)?:\/\/pan.baidu.com\/mbox\/homepage\?short=[a-zA-Z0-9]{4,10}')
    y = set(map(lambda x:x.get_text(),[link for link in links]))
    z=[]
    for y1 in y:
        y1 = pattern.findall(y1)
        if len(y1):
            y1 = y1[0]
            z.append(y1)
    z = set(z)
    link_we_need = z - x
    for link in link_we_need:
        link = pattern.findall(link)
        data = {
            'url':link[0]
        }
        groups.insert_one(data)
        print(data)


if __name__ == '__main__':
    get_threads(url)
    thread_urls = threads.find()
    for thread_url in thread_urls:
        thread_url = thread_url['url']
        get_group_links(thread_url)
