from selenium import webdriver
from urllib.parse import urlparse
import re

def get_title(driver):
    title = driver.find_element_by_xpath(r'//*[@id="content"]/div[@class="end_head"]/h2').text
    if title.endswith(']'):
        return ''.join(title.split()[:-1])
    return title

def get_sex(driver):
    big = driver.find_element_by_css_selector(r'#pieChart > svg > path:nth-child(3)').get_attribute('fill').replace('#5f9dfe','man').replace('#fc4e32','woman')
    big = (big, driver.find_element_by_xpath(r'//*[@id="pieChart"]/span[@class="data_value_big"]').text)

    small = driver.find_element_by_css_selector(r'#pieChart > svg > path:nth-child(4)').get_attribute('fill').replace('#5f9dfe','man').replace('#fc4e32','woman')
    small = (small, driver.find_element_by_xpath(r'//*[@id="pieChart"]/span[@class="data_value_small"]').text)

    return big, small
    
def get_age(driver):
    teens = driver.find_element_by_xpath(r'//*[@id="barChart"]/span[1]').text.replace('%','')
    twentys = driver.find_element_by_xpath(r'//*[@id="barChart"]/span[2]').text.replace('%','')
    thirtys = driver.find_element_by_xpath(r'//*[@id="barChart"]/span[3]').text.replace('%','')
    fortys = driver.find_element_by_xpath(r'//*[@id="barChart"]/span[4]').text.replace('%','')
    over_fifty = driver.find_element_by_xpath(r'//*[@id="barChart"]/span[5]').text.replace('%','')

    return teens,twentys,thirtys,fortys,over_fifty

get_id = lambda s : int(re.findall(r'\d+', s)[0])
get_author = lambda driver: driver.find_element_by_xpath(r'//*[@id="content"]/ul[1]/li/ul/li[3]/a').text
get_genre = lambda driver: driver.find_element_by_xpath(r'//*[@id="content"]/ul[1]/li/ul/li[2]/span').text
get_last_serial_day = lambda driver: driver.find_element_by_xpath(r'//*[@id="volumeList"]/tr[1]/td[1]/div/em').text
get_total_serial_count = lambda driver: driver.find_element_by_xpath(r'//*[@id="content"]/h5[@class="end_total_episode"]/strong').text
get_rating = lambda driver: driver.find_element_by_xpath(r'//*[@id="content"]/div[@class="end_head"]/div[@class="score_area"]/em').text

class Crawler:
    driver_path = r'c:\chromedriver.exe'
    all_genre_base_url = r'https://series.naver.com/novel/categoryProductList.nhn?categoryTypeCode=all&page='
    novel_base_url = r'https://series.naver.com/novel/detail.nhn?productNo='
    max_page = 2067
    id_list = []

    def __init__(self):
        self.id_list = []
        self.crawl_data = []

    def crawl(self, test = True):
        if test == True:
            max_page = 3

        driver = webdriver.Chrome(self.driver_path)
        
        #Get novel list from all genre
        for i in range(1, max_page+1):
            driver.get(self.all_genre_base_url + str(i))
            driver.implicitly_wait(10)
            novels = driver.find_elements_by_css_selector('#content > div > ul > li > a')
            for novel in novels:
                parts = urlparse(novel.get_attribute('href'))
                self.id_list.append(get_id(parts.query))
        
        for id in self.id_list:

            driver.get(self.novel_base_url + str(id))
            driver.implicitly_wait(10)

            title = get_title(driver)
            author = get_author(driver)
            genre = get_genre(driver)
            last_serial_day = get_last_serial_day(driver)
            total_serial_count = get_total_serial_count(driver)
            rating = get_rating(driver)
            age_ratio = None
            sex_ratio = None
            try:
                age_ratio = get_age(driver)
            except:
                pass
            try:
                sex_ratio = get_sex(driver)
            except:
                pass
                    

            self.crawl_data.append([id, title, author, genre, last_serial_day, total_serial_count, rating, sex_ratio, age_ratio])
        
        print(self.crawl_data)