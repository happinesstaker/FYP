from boilerpipe.extract import Extractor
import datetime
import feedparser
import hashlib
import json
import urllib2

import DBOperation


def GOOGLE_crawler():
    companies = dict()
    with open("target_companies.json","r") as infile:
        companies = json.load(infile)
    for company in companies["all_companies"]:
        GOOGLE_get_data(company)


def GOOGLE_get_data(company):

    google_news_rss_url = "https://news.google.com/news/?q=%s&output=rss" % company
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
        now = datetime.datetime.now()
        content_list.append({"title": title[:FYPsetting.TITLE_LEN_LIMIT].encode("UTF-8"),
                            "article": content[:FYPsetting.CONTENT_LEN_LIMIT].encode("UTF-8"),
                            "link": link[:FYPsetting.LINK_LEN_LIMIT],
                            "source": "GOOGLE",
                            "date": "%04d%02d%02d" % (now.year, now.month, now.day),
                            "hash": hashlib.sha224(title.encode("UTF-8")).hexdigest()})
                            

    DBOperation.save_db(content_list)

if __name__ == '__main__':
    GOOGLE_crawler()