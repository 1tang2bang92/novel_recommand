import time
import re

import requests
from bs4 import BeautifulSoup

def getSoup(url: str):
    res = requests.get(url)
    return BeautifulSoup(res.text, 'html.parser')

def getList(soup: BeautifulSoup):
    return soup.select('.dot_line')

def getTitle(soup: BeautifulSoup):
    return soup.select_one('a').text.strip()

def getAuthor(soup: BeautifulSoup):
    return soup.select_one('.member_nickname').text.strip()

def getView(soup: BeautifulSoup):
    return re.sub(r'[^0-9]', '',soup.parent.next_sibling.next_sibling.select_one('.btnR').text.split(':')[1].replace('\\[^0-9]\\',''))

def getRecommand(soup: BeautifulSoup):
    return re.sub(r'[^0-9]', '',soup.parent.next_sibling.next_sibling.select_one('.btnR').text.split(':')[3].replace('\\[^0-9]\\',''))
    
def getNum(soup: BeautifulSoup):
    return re.sub(r'[^0-9]', '',soup.select_one('a').next_sibling)

def getGenre(soup: BeautifulSoup):
    return soup.select_one('.cate').text


class Crawler:
    baseurl = 'http://www.joara.com'
    url = 'http://www.joara.com/literature/view/book_list.html?page_no='

    def __init__(self):
        self.list = []

    def crawl(self, num):
        soup = getSoup(self.url + str(num))
        novelList = getList(soup)
        for x in novelList:
            #print(x)
            title = getTitle(x)
            author = getAuthor(x)
            view = getView(x)
            recommand = getRecommand(x)
            num = getNum(x)
            genre = getGenre(x)
            print(genre, title, author, view, recommand, num)
            time.sleep(0)