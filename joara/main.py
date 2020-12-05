import multiprocessing as mp

from crawler import Crawler

genres = ['fantasy', 'love', 'rofan', 'muhyep', 'fusion', 'game', 'history', 'sports', 'ltnovel', 'bl', 'gl']

if __name__ == "__main__":
    for x in range(1, 10):
        Crawler().crawl(x, genres[0])