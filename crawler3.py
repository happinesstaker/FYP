__author__ = 'YANG'

import urllib2
import json
from BeautifulSoup import BeautifulSoup
from boilerpipe.extract import Extractor

def NASDAQ_crawler():

    symbol = 'csco' #Cisco
    url = 'http://www.nasdaq.com/symbol/'+symbol+'/news-headlines'

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
        content_list.append({"title": title, "article": content})

    with open(symbol+".NASDAQ.json", "w") as js_file:
        json.dump(content_list, js_file)

if __name__ == '__main__':
    NASDAQ_crawler()