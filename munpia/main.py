import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

numPool = 72
crawler = None

def onCrawlEnd(result):
    global data
    print(result)
    if result != None:
        data[result[0]] = result[1]

def execute(idx):
    global crawler
    if crawler == None:
        crawler = Crawler()

    return crawler.Crawl(idx)

class Crawler:
    url = "https://novel.munpia.com/"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.driver = webdriver.Chrome('C:\\chromedriver.exe',options=options)
        self.wait = WebDriverWait(self.driver,2)        
    
    def GetData(self, num):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='error'']")))
            return None
        except:
            pass
        
        title = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='board']/div[1]/div[3]/h2/a")))
        args = title.text.split('\n')
        length = len(args)

        if length == 1:
            title = args[0].replace(",","")
        else:
            title = args[1].replace(",","")

        writer = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='board']/div[1]/div[3]/dl[1]/dd"))).text.replace(",","")
        genre = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='board']/div[1]/div[3]/p[1]/strong"))).text.replace(",","")
        viewsNumber = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='board']/div[1]/div[3]/dl[3]/dd[2]"))).text.replace(",","").replace(",","")
        recommendNumber = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='board']/div[1]/div[3]/dl[3]/dd[3]"))).text.replace(",","").replace(",","")
        serializatNumber = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='board']/div[1]/div[3]/dl[3]/dd[1]"))).text.replace("회","").replace(",","")
        man = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='left-chart']/div/div[1]/div/div/table/tbody/tr[1]/td[2]"))).get_attribute("innerText").replace(",","") # 크롬 드라이버 자체 오류
        woman = self.wait.until(EC.presence_of_element_located((By.XPATH, " //*[@id='left-chart']/div/div[1]/div/div/table/tbody/tr[2]/td[2]"))).get_attribute("innerText").replace(",","")

        nman = int(man)
        nwoman = int(woman)

        if nman>nwoman:
            sex = "남자"
        elif nwoman>nman:
            sex = "여자"
        else:
           sex = "같음"

        age = []

        age.append(int(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="right-chart"]/div/div[1]/div/div/table/tbody/tr[1]/td[2]'))).get_attribute("innerText").replace(",","")))
        age.append(int(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="right-chart"]/div/div[1]/div/div/table/tbody/tr[2]/td[2]'))).get_attribute("innerText").replace(",","")))
        age.append(int(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="right-chart"]/div/div[1]/div/div/table/tbody/tr[3]/td[2]'))).get_attribute("innerText").replace(",","")))
        age.append(int(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="right-chart"]/div/div[1]/div/div/table/tbody/tr[4]/td[2]'))).get_attribute("innerText").replace(",","")))
        age.append(int(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="right-chart"]/div/div[1]/div/div/table/tbody/tr[5]/td[2]'))).get_attribute("innerText").replace(",","")))

        s_age = sorted(age,reverse=True)

        for index, value in enumerate(age):
            if s_age[0] == value:
                age =  str((index+1)*10).replace(",","")

        if '' in [title,writer,genre,sex,viewsNumber,recommendNumber,serializatNumber,age]:
            return None

        return (num, title +","+  writer+","+genre+","+sex+","+ viewsNumber+","+recommendNumber+","+serializatNumber+","+age +"\n")

    def Crawl(self, num):
        self.driver.get(self.url + str(num))
        print(num)
        return self.GetData(num)

    def quit(self):
        self.driver.quit()

if __name__ == "__main__":
    global data

    data = {}
    pool = mp.Pool(processes=numPool)

    for i in range(1, 250000):
        pool.apply_async(execute, args=(i, ), callback=onCrawlEnd)

    pool.close()
    pool.join()

    file = open("Data.csv", "w")

    file.write('title,author,genre,sex,view,recommandation_count,avg_serial_num,preferred_age')
    for i in data.values():
        file.write(i)
    file.flush()

    print("crowling done")