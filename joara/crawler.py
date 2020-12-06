import time
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getSoup(url: str):
    res = requests.get(url)
    return BeautifulSoup(res.text, 'html.parser')

def getList(soup: BeautifulSoup):
    return soup.select('.dot_line')

def getUrl(soup: BeautifulSoup):
    return 'http://www.joara.com' + soup.select_one('a').attrs['href']

def getWork(url):
    if 'literature' in url:
        return 'Literature'
    elif 'nobless' in url:
        return 'Nobless'
    elif 'premium' in url:
        return 'Premium'
    elif 'romancebl' in url:
        return 'Romance'
    elif 'finish' in url:
        return 'Finish'
    
def getTitle(soup: BeautifulSoup):
    return soup.select_one('a').text.strip()

def getAuthor(soup: BeautifulSoup):
    return soup.select_one('.member_nickname').text.strip()

def getGenre(soup: BeautifulSoup):
    return list(map(lambda x: x[:-1], soup.select_one('.cate').text.split('[')))[1:]

def getView(soup: BeautifulSoup):
    return int(re.sub(r'[^0-9]', '',soup.parent.next_sibling.next_sibling.select_one('.btnR').text.split(':')[1].replace('\\[^0-9]\\','')))

def getRecommand(soup: BeautifulSoup):
    return int(re.sub(r'[^0-9]', '',soup.parent.next_sibling.next_sibling.select_one('.btnR').text.split(':')[3].replace('\\[^0-9]\\','')))
    
def getLastDate(soup: BeautifulSoup):
    return soup.select('span')[4].text.strip().split(' ')[0]

def getNum(soup: BeautifulSoup):
    return int(re.sub(r'[^0-9]', '',soup.select_one('a').next_sibling))


class Crawler:
    url = 'http://www.joara.com/literature/view/book_list.html'
    page = 'page_no='
    genre = 'sl_category='

    def __init__(self):
        self.list = []
        options = Options()
        options.set_headless(True)
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)


    def getTitle(self, work):
        if work == 'Nobless':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'fTit')))[0]
            return elem.text.strip()
        elif work == 'Literature':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.work_tit a')))[0]
            return elem.get_attribute('title').strip()
        else:
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ico_new a')))[0]
            return elem.text.strip()

    def getSize(self, work):
        if work == 'Nobless':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.bookValue .flistCon')))[0]
            return float(re.sub('[^0-9.]', '', elem.text)) * 1024
        elif work == 'Premium':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.info .date')))[1]
            return float(re.sub('[^0-9.]', '', elem.text)) * 1024
        elif work == 'Finish':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.info .date')))[1]
            return float(re.sub('[^0-9.]', '', elem.text)) * 1024
        else:
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'work_view')))[0]
            text = elem.text
            text = text[text.find('작품용량'):]
            return float(re.sub('[^0-9.]', '', text)) * 1024

    def getStartDate(self, work):
        if work == 'Nobless':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.writerAct .flistCon')))[0]
            return re.sub('[^0-9.]', '', elem.text.split('/')[1])
        elif work == 'Premium':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tbl_work tbody tr:last-child td:nth-child(4) a')))[0]
            return elem.text.strip().replace('/', '.')
        elif work == 'Finish':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tbl_work tbody tr:last-child td:nth-child(4) a')))[0]
            return elem.text.strip().replace('/', '.')
        else:
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.info .date:last-child')))[0]
            return re.sub('[^0-9.]', '', elem.text)            

    def crawl(self, num):
        soup = getSoup(self.url + '?' + self.page + str(num))
        novelList = getList(soup)
        for elem in novelList:
            url = getUrl(elem)
            self.driver.get(url)

            url = self.driver.current_url

            print(url)

            work = getWork(url)
            
            title = self.getTitle(work)
            author = getAuthor(elem)
            genre = getGenre(elem)
            view = getView(elem)
            recommand = getRecommand(elem)
            size = self.getSize(work)
            startDate = self.getStartDate(work)
            lastDate = getLastDate(elem)

            print(work, title, author, genre,view, recommand, size, startDate, lastDate)
            time.sleep(0)