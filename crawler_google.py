__author__ = 'Jiajie YANG'

from boilerpipe.extract import Extractor
import feedparser
import hashlib
import json
import urllib2

import DBOperation
import FYPsetting

def GOOGLE_crawler():
    google_news_rss_url = "https://news.google.com/news/?q=%s&output=rss" % FYPsetting.NASDAQ_CONFIG["company"]
    rss_feed = feedparser.parse(google_news_rss_url)

    content_list = list()

    for entry in rss_feed['entries']:
        title = entry['title']
        link = entry['link']
        try:
            news_page = urllib2.urlopen(link).read()
            extractor = Extractor(extractor='ArticleExtractor', html=news_page)
        except:
            continue
        content = extractor.getText()
        content_list.append({"title": title[:290],
                            "article": content[:2950],
                            "link": link[:290],
                            "source": "GOOGLE",
                            "hash": hashlib.sha224(title.encode("UTF-8")).hexdigest()})

    DBOperation.save_db(content_list)

if __name__ == '__main__':
    GOOGLE_crawler()