__author__ = 'Jiajie YANG'

from boilerpipe.extract import Extractor
from twitter import *
import hashlib
import json

import FYPsetting
import DBOperation

def Twitter_crawler():
    company = FYPsetting.TWITTER_CONFIG["company"]
    config = FYPsetting.TWITTER_CONFIG
    
    twitter = Twitter(auth=OAuth(config["access_key"], config["access_secret"],
                                    config["consumer_key"], config["consumer_secret"]))
    query = twitter.search.tweets(q=company, lang="en", result_type="recent", count="%d" % FYPsetting.QUERY_PAGE)
    
    urllist = list()
    content_list = list()
    
    for result in query["statuses"]:
        #print "@%s %s" % (result["user"]["screen_name"].encode("UTF-8"), result["text"].encode("UTF-8"))
        cur_text = result["text"].split(" ")
        for word in cur_text:
            if word.startswith("http"):
                utf_word = word.encode("UTF-8")
                if utf_word in urllist:
                    break
                urllist.append(utf_word)
    
                try:
                    extractor = Extractor(extractor='ArticleExtractor', url=utf_word)
                except:
                    break
                content = extractor.getText()
                if content is not "":
                    content_list.append({"title": (result["text"].encode("UTF-8"))[:290],
                                        "article": (content.encode("UTF-8"))[:2950],
                                        "link":utf_word, "source": "TWITTER",
                                        "hash": hashlib.sha224(result["text"].encode("UTF-8")).hexdigest()})
                break
    
    DBOperation.save_db(content_list)

if __name__ == '__main__':
    Twitter_crawler()