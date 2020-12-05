import time
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
        return None
    elif 'nobless' in url:
        return 'Nobless'
    elif 'premium' in url:
        return 'Premium'
    elif 'romancebl' in url:
        return 'Romance'
    
def getTitle(soup: BeautifulSoup):
    return soup.select_one('a').text.strip()

def getAuthor(soup: BeautifulSoup):
    return soup.select_one('.member_nickname').text.strip()

def getGenre(soup: BeautifulSoup):
    return soup.select_one('.cate').text

def getView(soup: BeautifulSoup):
    return re.sub(r'[^0-9]', '',soup.parent.next_sibling.next_sibling.select_one('.btnR').text.split(':')[1].replace('\\[^0-9]\\',''))

def getRecommand(soup: BeautifulSoup):
    return re.sub(r'[^0-9]', '',soup.parent.next_sibling.next_sibling.select_one('.btnR').text.split(':')[3].replace('\\[^0-9]\\',''))
    
def getNum(soup: BeautifulSoup):
    return re.sub(r'[^0-9]', '',soup.select_one('a').next_sibling)


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
        elif work == 'Premium':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ico_new a')))[0]
            return elem.text.strip()
        elif work == 'Romance':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ico_new a')))[0]
            return elem.text.strip()
        else:
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.work_tit a')))[0]
            return elem.get_attribute('title').strip()

    def getAuthor(self, work):
        if work == 'Nobless':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'fWriter')))[0]
            return elem.text.strip()
        else:
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'writer')))[0]
            return elem.text.strip()

    def getGenre(self, work):
        if work == 'Nobless':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'fGenre')))[0]
            return elem.text.strip()
        elif work == 'Premium':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'b_tits')))[0]
            return elem.text.strip()
        else:
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.title h3 img')))[0]
            return elem.get_attribute('alt').strip()

    def getView(self, work):
        if work == 'Nobless':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'flistCon')))[0]
            text = elem.text.split('|')[0]
            return re.sub('[^0-9]', '', text)
        else:
            elem = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="info2"]/span[1]')))[0]
            return elem.text.strip().replace(',', '')

    def getRecommand(self, work):
        if work == 'Nobless':
            elem = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'flistCon')))[0]
            text = elem.text.split('|')[1]
            return re.sub('[^0-9]', '', text)
        else:
            elem = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="info2"]/span[3]')))[0]
            return elem.text.strip().replace(',', '')

    def crawl(self, num):
        soup = getSoup(self.url + '?' + self.page + str(num))
        novelList = getList(soup)
        for elem in novelList:
            url = getUrl(elem)
            self.driver.get(url)

            url = self.driver.current_url
            work = getWork(url)
            
            title = self.getTitle(work)
            author = getAuthor(elem)
            genre = getGenre(elem)
            view = getView(elem)
            recommand = getRecommand(elem)

            print(work, title, author, genre,view, recommand)

            #num = getNum(soup)
            #print(title)
            time.sleep(1)