
import time
import requests
import sqlite3
from bs4 import BeautifulSoup
import re
import threading
import multiprocessing
from hashlib import sha256 as SHA256
import os
import datetime
from dateutil.parser import parse as parsedate
import random

TIME = 4.0
DARK_TIME = 10.0
MULTIPLY = 128
CACHE = 'cache.ch'
user_agents = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def site_sweep(url):
    try:
        r = requests.get(url)
        txt = r.text
        ans = []
        addrs = re.findall("[13][a-km-zA-HJ-NP-Z1-9]{25,33}", txt)
        for addr in addrs:
            version = addr[0]
            checksum = addr[-4:]
            vh160 = addr[:-4]  # Version plus hash160 is what is checksummed
            h3 = SHA256(SHA256(vh160).digest()).digest()
            if h3[0:4] == checksum:
                ans.append(addr)
        print(ans)
        return ans
    except Exception as e:
        print(e)
        return [str(e)]


def multi_addr(lst):
    ans = []
    for item in lst:
        p = CrawlerQueue(ttl=150, query=item)
        p.start()
        ans.append(p.output())
    return ans


def is_modified(url, dstFile):
    r = requests.head(url)
    try:
        url_time = r.headers['last-modified']
        url_date = parsedate(url_time)
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(dstFile))
        return url_date.timestamp() > file_time.timestamp()
    except:
        return True


def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))

    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)


def check_cache(url):
    fd = open(CACHE, 'r')
    inst = fd.readlines()
    fd.close()
    return url in inst


def add_cache(url):
    fd = open(CACHE, 'a')
    fd.write(url + '\n')
    fd.close()


def del_cache():
    fd = open(CACHE, 'w')
    fd.write('')
    fd.close()


'''Crawler V.1'''

''' legacy crawler'''


class Crawler:
    def __init__(self, ttl=1, query='none'):
        self.url_root = sqlite3.connect('database.db')
        self.pages = self.url_root.cursor().execute("SELECT * FROM urls")
        self.ttl = ttl
        self.query = query
        self.result = []
        for page in self.pages:
            self.search(page[0], self.ttl)

    def search(self, page, ttl):
        try:
            code = requests.get(page, timeout = TIME).text
        except Exception as e:
            print(e)
            code = ""
        soup = BeautifulSoup(code, 'html.parser')

        if soup.find(self.query) is not []:
            self.result.append(page)
        if ttl > 0:
            for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                print(link.get('href'))
                t = threading.Thread(target=self.search, args=[link.get('href'), ttl-1])
                # self.search(link.get('href'), ttl-1)
                t.start()

    def output(self):
        return self.result


def getsite(site):
    stopindex = site.find('.com')
    return site[0:(stopindex+4)]


def getdarksite(site):
    stopindex = site.find('.onion')
    return site[0:(stopindex + 4)]


class CrawlerQueue:
    def __init__(self, ttl=1, query='none'):
        self.url_root = sqlite3.connect('database.db')
        self.pages = self.url_root.cursor().execute("SELECT * FROM urls")
        self.ttl = ttl
        self.query = query
        self.result = []
        self.pageQueue = []
        for page in self.pages:
            if page[0][-2:] == 'q=' or page[0][-8:] == 'address/':
                self.pageQueue.append(page[0] + query)
            else:
                self.pageQueue.append(page[0])

    def start(self):
        if os.path.isfile(CACHE):
            pass
        else:
            f = open(CACHE, 'w')
            f.close()
        for cpu in range(MULTIPLY*multiprocessing.cpu_count()):
            t = threading.Thread(target=self.searchByQueue)
            t.setName("thread " + str(cpu))
            t.start()
        t = threading.Thread(target=self.config)
        t.setName("config")
        t.start()

    def config(self):
        while threading.active_count() > 4:
            print(str(threading.active_count()) + ', ' + str(self.ttl))
            time.sleep(1.0)

    def resume(self):
        f = open('cache.ch', 'r')
        self.pageQueue = f.readlines()
        f.close()
        for cpu in range(MULTIPLY*multiprocessing.cpu_count()):
            t = threading.Thread(target=self.searchByQueue)
            t.setName("thread " + str(cpu))
            t.start()
        while threading.active_count() > 2:
            print(str(threading.active_count()) + ', ' + str(self.ttl))
            time.sleep(1.0)

    def searchByQueue(self):
        if len(self.pageQueue) == 0:
            if threading.active_count() > 2 and self.ttl > 0:
                time.sleep(TIME)
            else:
                pass
        else:
            page = self.pageQueue.pop(0)
            # self.cache = open('cache.ch', 'r')
            # lst = self.cache.readlines()
            # self.cache.close()
            '''
            if page+'\n' in lst:
                print("in cache")
                self.ttl -= 1
            else:
            '''
            try:
                dict = {'://': '.', '/': '.', '?': '.', '=': '.', '&': '.'}
                path = 'index\\' + multiple_replace(dict, page) + '.html'
                # page.replace('://', '.').replace('/', '.').replace() + '.html'
                if not check_cache(page):
                    if os.path.isfile(path):
                        if is_modified(page, path):
                            print("file modified "+page)
                            if page.find("reddit") != -1:
                                time.sleep(8)
                                print("awake")
                            code = requests.get(page, timeout=TIME, headers={'User-Agent':random.choice(user_agents)}).text
                            fd = open(path, 'r+', encoding="utf-8")
                            if code != '':
                                fd.write(code)
                            fd.close()
                        else:
                            print('time saved ' + page)
                            fd = open(path, 'r', encoding="utf-8")
                            code = fd.read()
                            fd.close()
                    else:
                        print("indexing... " + page)
                        code = requests.get(page, timeout=TIME).text
                        if code != '':
                            fd = open(path, 'w+', encoding="utf-8")
                            try:
                                fd.write(code)
                            except:
                                pass
                            fd.close()
                    soup = BeautifulSoup(code, 'html.parser')
                    if re.findall(self.query, code) != []:
                        if page.find("reddit") != -1:
                            print("result: " + str(code))
                        print(page)
                        self.result.append(page)
                    for link in soup.findAll('a', href=True):
                        link = link.get('href')
                        if link[0:5] not in ['https', 'http:']:
                            link = getsite(page) + link
                        self.pageQueue.append(link)
                    add_cache(page)
                else:
                    print('in cache-time saved')
            except Exception as e:
                print(e)
            self.ttl -= 1

        if self.ttl > 0:
            self.searchByQueue()
        else:
            pass

    def output(self):
        del_cache()
        while not threading.active_count() <= 5:
            pass
        return self.result


class DarkCrawler:
    def __init__(self, ttl=1, query='none'):
        self.url_root = sqlite3.connect('database.db')
        self.pages = self.url_root.cursor().execute("SELECT * FROM onions")
        self.session = requests.session()
        self.session.proxies = {}
        self.session.proxies['http'] = 'socks5h://localhost:9050'
        self.session.proxies['https'] = 'socks5h://localhost:9050'
        self.ttl = ttl
        self.query = query
        self.result = []
        self.pageQueue = []
        for page in self.pages:
            if page[0][-2:] == 'q=' or page[0][-8:] == 'address/':
                self.pageQueue.append(page[0] + query)
            else:
                self.pageQueue.append(page[0])

    def start(self):
        if os.path.isfile(CACHE):
            pass
        else:
            f = open(CACHE, 'w')
            f.close()
        for cpu in range(MULTIPLY*multiprocessing.cpu_count()):
            t = threading.Thread(target=self.searchByQueue)
            t.setName("thread " + str(cpu))
            t.start()
        t = threading.Thread(target=self.config)
        t.setName("config")
        t.start()

    def config(self):
        while threading.active_count() > 4:
            print(str(threading.active_count()) + ', ' + str(self.ttl))
            time.sleep(1.0)

    def resume(self):
        f = open('cache.ch', 'r')
        self.pageQueue = f.readlines()
        f.close()
        for cpu in range(MULTIPLY*multiprocessing.cpu_count()):
            t = threading.Thread(target=self.searchByQueue)
            t.setName("thread " + str(cpu))
            t.start()
        while threading.active_count() > 2:
            print(str(threading.active_count()) + ', ' + str(self.ttl))
            time.sleep(1.0)

    def searchByQueue(self):
        if len(self.pageQueue) == 0:
            if threading.active_count() > 2 and self.ttl > 0:
                time.sleep(TIME)
            else:
                pass
        else:
            page = self.pageQueue.pop(0)
            # self.cache = open('cache.ch', 'r')
            # lst = self.cache.readlines()
            # self.cache.close()
            '''
            if page+'\n' in lst:
                print("in cache")
                self.ttl -= 1
            else:
            '''
            try:
                dict = {'://': '.', '/': '.', '?': '.', '=': '.', '&': '.'}
                path = 'index\\' + multiple_replace(dict, page) + '.html'
                # page.replace('://', '.').replace('/', '.').replace() + '.html'
                if not check_cache(page):
                    if os.path.isfile(path):
                        if is_modified(page, path):
                            print("file modified "+page)
                            if page.find("reddit") != -1:
                                time.sleep(8)
                                print("awake")
                            code = self.session.get(page, timeout=TIME, headers={'User-Agent':random.choice(user_agents)}).text
                            fd = open(path, 'r+', encoding="utf-8")
                            if code != '':
                                fd.write(code)
                            fd.close()
                        else:
                            print('time saved ' + page)
                            fd = open(path, 'r', encoding="utf-8")
                            code = fd.read()
                            fd.close()
                    else:
                        print("indexing... " + page)
                        code = self.session.get(page, timeout=TIME).text
                        if code != '':
                            fd = open(path, 'w+', encoding="utf-8")
                            try:
                                fd.write(code)
                            except:
                                pass
                            fd.close()
                    soup = BeautifulSoup(code, 'html.parser')
                    if re.findall(self.query, code) != []:
                        if page.find("reddit") != -1:
                            print("result: " + str(code))
                        print(page)
                        self.result.append(page)
                    for link in soup.findAll('a', href=True):
                        link = link.get('href')
                        if link[0:5] not in ['https', 'http:']:
                            link = getsite(page) + link
                        self.pageQueue.append(link)
                    add_cache(page)
                else:
                    print('in cache-time saved')
            except Exception as e:
                print(e)
            self.ttl -= 1

        if self.ttl > 0:
            self.searchByQueue()
        else:
            pass

    def output(self):
        del_cache()
        while not threading.active_count() <= 8:
            pass
        return self.result
