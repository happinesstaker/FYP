from boilerpipe.extract import Extractor
from BeautifulSoup import BeautifulSoup
import datetime
import hashlib
import json
import urllib2

import DBOperation


def NASDAQ_crawler():
    companies = dict()
    with open("target_companies.json","r") as infile:
        companies = json.load(infile)
    for company in companies["company_code"]:
        NASDAQ_get_data(company)

def NASDAQ_get_data(company_code):

    url = 'http://www.nasdaq.com/symbol/%s/news-headlines' % company_code
    
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
        #print title
        try:
            news_page = urllib2.urlopen(link).read()
            extractor = Extractor(extractor='ArticleExtractor', html=news_page)
        except:
            continue
        content = extractor.getText()
        now = datetime.datetime.now()
        content_list.append({"title": title[:FYPsetting.TITLE_LEN_LIMIT],
                            "article": content[:FYPsetting.CONTENT_LEN_LIMIT],
                            "link": link[:FYPsetting.LINK_LEN_LIMIT],
                            "source": "NASDAQ",
                            "date": "%04d%02d%02d" % (now.year, now.month, now.day),
                            "hash": hashlib.sha224(title.encode("UTF-8")).hexdigest()})
    
    DBOperation.save_db(content_list)

if __name__ == '__main__':
    NASDAQ_crawler()