from boilerpipe.extract import Extractor
from BeautifulSoup import BeautifulSoup
import datetime
import hashlib
import json
import urllib2
import os

import DBOperation
import FYPsetting


def NASDAQ_crawler():
    companies = dict()
    with open("%s/target_companies.json" % os.path.dirname(os.path.realpath(__file__)),"r") as infile:
        companies = json.load(infile)
    for company in companies["company_code"]:
        NASDAQ_get_data(company)

def NASDAQ_get_data(company_code):

    url = 'http://www.nasdaq.com/symbol/%s/news-headlines' % company_code
    
    conn = urllib2.urlopen(url)
    html = conn.read()
    
    soup = BeautifulSoup(html)
    content_div = soup.find("div", {'class': "news-headlines"})
    
    # No news found?
    if content_div==None:
        return
        
    links = content_div.findAll('a')
    
    content_list = list()
    
    for tag in links:
        if tag.parent.name != "span":
            continue
        link = tag.get('href', None)
        title = tag.contents[0]
        try:
            news_page = urllib2.urlopen(link).read()
            extractor = Extractor(extractor='ArticleExtractor', html=news_page)
        except:
            continue
        content = extractor.getText()
        now = datetime.datetime.now()
        content_list.append({"title": title,
                            "article": content,
                            "link": link,
                            "source": "NASDAQ",
                            "target": company_code,
                            "date": "%04d%02d%02d" % (now.year, now.month, now.day),
                            "hash": hashlib.sha224(title.encode("UTF-8")).hexdigest()})
    
    DBOperation.save_db(content_list)

if __name__ == '__main__':
    NASDAQ_crawler()