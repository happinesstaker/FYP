__author__ = 'Jiajie YANG'

from boilerpipe.extract import Extractor
import cookielib
import hashlib
import json
import requests
import urllib2

import FYPsetting
import DBOperation

def NYT_crawler():
    raw_response_list = list()
    API_base_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?"
    config = FYPsetting.NYT_CONFIG
    
    for page in range(FYPsetting.QUERY_PAGE//3):
        url = "%sbegin_data=%s&sort=newest&page=%d&q=%s&api-key=%s" % (API_base_url, config["begin_date"], page, config["company"], config["API_key"])
        response = requests.get(url).json()
        raw_response_list += response["response"]["docs"]
    
    content_list = list()
    
    for doc in raw_response_list:
        url = doc["web_url"]
        title = doc["headline"]["main"]
        #print title
        try:
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            html = opener.open(url).read()
            extractor = Extractor(extractor='ArticleExtractor', html=html)
        except:
            continue
        content = extractor.getText()
        content_list.append({"title": title[:290],
                            "article": content[:2950],
                            "link": url[:290],
                            "source": "NYT",
                            "hash": hashlib.sha224(title.encode("UTF-8")).hexdigest()})
    
    DBOperation.save_db(content_list)

if __name__ == '__main__':
    NYT_crawler()