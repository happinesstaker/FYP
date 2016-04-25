from boilerpipe.extract import Extractor
import cookielib
import datetime
import hashlib
import json
import requests
import urllib2
import os

import FYPsetting
import DBOperation


def NYT_crawler():
    companies = dict()
    with open("%s/target_companies.json" % os.path.dirname(os.path.realpath(__file__)),"r") as infile:
        companies = json.load(infile)
    for company in companies["all_companies"]:
        NYT_get_data(company)


def NYT_get_data(company):
    raw_response_list = list()
    API_base_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?"
    config = FYPsetting.NYT_CONFIG
    
    now = datetime.datetime.now()
    past = now - datetime.timedelta(hours=72)
    now_str = "%04d%02d%02d" % (now.year, now.month, now.day)
    past_str = "%04d%02d%02d" % (past.year, past.month, past.day)
    
    for page in range(FYPsetting.QUERY_PAGE//3):
        url = "%sbegin_data=%s&sort=newest&page=%d&q=%s&api-key=%s" % (API_base_url, past_str, page, company, config["API_key"])
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
        now = datetime.datetime.now()
        content_list.append({"title": title,
                            "article": content,
                            "link": url,
                            "source": "NYT",
                            "target": company,
                            "date": now_str,
                            "hash": hashlib.sha224(title.encode("UTF-8")).hexdigest()})
    
    DBOperation.save_db(content_list)

if __name__ == '__main__':
    NYT_crawler()