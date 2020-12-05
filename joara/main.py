import multiprocessing as mp

from crawler import Crawler

genres = ['fantasy', 'love', 'rofan', 'muhyep', 'fusion', 'game', 'history', 'sports', 'ltnovel', 'bl', 'gl']

if __name__ == "__main__":
    for x in range(1, 2):
        Crawler().crawl(4)