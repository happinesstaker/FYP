__author__ = 'Jiajie YANG'

from boilerpipe.extract import Extractor
from BeautifulSoup import BeautifulSoup
import hashlib
import json
import urllib2

import FYPsetting
import DBOperation

def NASDAQ_crawler():

    url = 'http://www.nasdaq.com/symbol/%s/news-headlines' % FYPsetting.NASDAQ_CONFIG["company"]
    
    conn = urllib2.urlopen(url)
    html = conn.read()
    
    soup = BeautifulSoup(html)
    content_div = soup.find("div", {'class': "headlines"})
    links = content_div.findAll('a')
    
    content_list = list()
    
    for tag in links:
        if tag.parent.name == "small":
            continue
        link = tag.get('href', None)
        title = tag.contents[0]
        print title
        try:
            news_page = urllib2.urlopen(link).read()
            extractor = Extractor(extractor='ArticleExtractor', html=news_page)
        except:
            continue
        content = extractor.getText()
        content_list.append({"title": title[:290],
                            "article": content[:2950],
                            "link": link[:290],
                            "source": "NASDAQ",
                            "hash": hashlib.sha224(title.encode("UTF-8")).hexdigest()})
    
    DBOperation.save_db(content_list)

if __name__ == '__main__':
    NASDAQ_crawler()