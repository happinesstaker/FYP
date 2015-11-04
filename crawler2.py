__author__ = 'Jiajie YANG'

import requests
import json
import urllib2
import cookielib
from boilerpipe.extract import Extractor

COMPANY2 = "cisco"
NY_API_KEY = 'dafd1e77c5a943648589c495de8e9d73:6:72720402'

raw_response_list = list()



for page in range(3):
    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?begin_data=20100101&sort=newest&page="+str(page)+"&q="+COMPANY2+"&api-key="+NY_API_KEY
    response = requests.get(url).json()
    raw_response_list += response["response"]["docs"]

content_list = list()

for doc in raw_response_list:
    url = doc["web_url"]
    title = doc["headline"]["main"]
    print title
    try:
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        html = opener.open(url).read()
        extractor = Extractor(extractor='ArticleExtractor', html=html)
    except:
        continue
    content = extractor.getText()
    content = content.replace("\n", " ")
    content_list.append({"title": title, "article": content})

with open(COMPANY2+".json", "w") as js_file:
    json.dump(content_list, js_file)

