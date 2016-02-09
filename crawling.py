import threading

from crawler_google import GOOGLE_crawler
from crawler_nasdaq import NASDAQ_crawler
from crawler_nyt import NYT_crawler
from crawler_twitter import Twitter_crawler

if __name__ == "__main__":
    thread_list = list()
    thread_list.append(threading.Thread(target = GOOGLE_crawler))
    thread_list.append(threading.Thread(target = NASDAQ_crawler))
    thread_list.append(threading.Thread(target = NYT_crawler))
    thread_list.append(threading.Thread(target = Twitter_crawler))

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()