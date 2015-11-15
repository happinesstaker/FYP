__author__ = 'YANG'

import urllib2
import json
import feedparser
from boilerpipe.extract import Extractor

COMPANY = "cisco"
google_news_rss_url = "https://news.google.com/news/?q="+COMPANY+"&output=rss"

rss_feed = feedparser.parse(google_news_rss_url)

content_list = list()

for entry in rss_feed['entries']:
    title = entry['title']
    print title
    link = entry['link']
    try:
        news_page = urllib2.urlopen(link).read()
        extractor = Extractor(extractor='ArticleExtractor', html=news_page)
    except:
        continue
    content = extractor.getText()
    content_list.append({"title": title, "article": content})

with open(COMPANY+".GOOGLE.json", "w") as js_file:
    json.dump(content_list, js_file)
