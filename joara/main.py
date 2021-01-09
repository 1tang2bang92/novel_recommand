import multiprocessing as mp

from crawler import Crawler
from db import DB

procNum = 10
genres = ['fantasy', 'love', 'rofan', 'muhyep', 'fusion', 'game', 'history', 'sports', 'ltnovel', 'bl', 'gl']
crawler = None
db = None

def workend(result):
    global db
    if not db:
        db = DB()
    print(result)
    if result:
        for x in result:
            db.insertData('joara', x)
            pass

def process(num):
    global crawler
    if not crawler:
        crawler = Crawler()
    return crawler.crawl(num) 

if __name__ == "__main__":
    pool = mp.Pool(procNum)

    for idx in range(1, 11):
        pool.apply_async(process, args=(idx, ), callback=workend)

    pool.close()
    pool.join()
