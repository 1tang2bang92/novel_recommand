from selenium import webdriver
from urllib.parse import urlparse

driver_path = r'c:\chromedriver.exe'
all_genre_base_url = r'https://series.naver.com/novel/categoryProductList.nhn?categoryTypeCode=all&page='
novel_base_url = r'https://series.naver.com/novel/detail.nhn?'
max_page = 2067
test = True

if __name__ == '__main__':

    if test == True:
        max_page = 3

    driver = webdriver.Chrome(driver_path)
    id_list = []

    #Get novel list from all genre
    for i in range(1, max_page+1):
        driver.get(all_genre_base_url + str(i))
        driver.implicitly_wait(10)
        novels = driver.find_elements_by_css_selector('#content > div > ul > li > a')
        for novel in novels:
            parts = urlparse(novel.get_attribute('href'))
            id_list.append(parts.query)
    
    for id in id_list:

        driver.get(novel_base_url + id)
        driver.implicitly_wait(10)

        title = driver.find_element_by_xpath('//*[@id="content"]/div[@class="end_head"]/h2').text
        author = driver.find_element_by_xpath('//*[@id="content"]/ul[1]/li/ul/li[3]/a').text
        genre = driver.find_element_by_xpath('//*[@id="content"]/ul[1]/li/ul/li[2]/span').text
        last_serial_day = driver.find_element_by_xpath('//*[@id="volumeList"]/tr[1]/td[1]/div/em').text
        total_serial_count = driver.find_element_by_xpath('//*[@id="content"]/h5[@class="end_total_episode"]/strong').text
        rating = driver.find_element_by_xpath('//*[@id="content"]/div[@class="end_head"]/div[@class="score_area"]/em').text

        print(title, author, genre, last_serial_day, total_serial_count, rating)
