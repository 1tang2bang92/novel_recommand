from selenium import webdriver
from urllib.parse import urlparse

def get_title(driver):
    title = driver.find_element_by_xpath('//*[@id="content"]/div[@class="end_head"]/h2').text
    if title.endswith(']'):
        return ''.join(title.split()[:-1])
    return title

get_author = lambda driver: driver.find_element_by_xpath('//*[@id="content"]/ul[1]/li/ul/li[3]/a').text
get_genre = lambda driver: driver.find_element_by_xpath('//*[@id="content"]/ul[1]/li/ul/li[2]/span').text
get_last_serial_day = lambda driver: driver.find_element_by_xpath('//*[@id="volumeList"]/tr[1]/td[1]/div/em').text
get_total_serial_count = lambda driver: driver.find_element_by_xpath('//*[@id="content"]/h5[@class="end_total_episode"]/strong').text
get_rating = lambda driver: driver.find_element_by_xpath('//*[@id="content"]/div[@class="end_head"]/div[@class="score_area"]/em').text

class Crawler:
    driver_path = r'c:\chromedriver.exe'
    all_genre_base_url = r'https://series.naver.com/novel/categoryProductList.nhn?categoryTypeCode=all&page='
    novel_base_url = r'https://series.naver.com/novel/detail.nhn?'
    max_page = 2067
    id_list = []

    def __init__(self):
        self.id_list = []

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
                self.id_list.append(parts.query)
        
        for id in self.id_list:

            driver.get(self.novel_base_url + id)
            driver.implicitly_wait(10)

            title = get_title(driver)
            author = get_author(driver)
            genre = get_genre(driver)
            last_serial_day = get_last_serial_day(driver)
            total_serial_count = get_total_serial_count(driver)
            rating = get_rating(driver)

            print(title, author, genre, last_serial_day, total_serial_count, rating)