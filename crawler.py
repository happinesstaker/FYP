__author__ = 'Jiajie YANG'

from twitter import *
import json
from boilerpipe.extract import Extractor

COMPANY = 'airbnb'
BoilerPipeURL = "http://boilerpipe-web.appspot.com/extract?output=text&url="

# Twitter source
config = {"access_key": "3780616332-PArbYD6xifva5Zo9oTUqg6yJlPwYa9WdR53Tdlk",
          "access_secret": "ccXRQorrexkTS3xpRYHJobT11eGA3i4MB6Bj7WezRvevO",
          "consumer_key": "RctxsgdWyhHpfNDIeUPAxKJ5f",
          "consumer_secret": "Lx4GAVULXCsFlHE50sw3m8Ca6w6IDK5hLkBCSCL7HSVtyQiJh2"}

twitter = Twitter(auth=OAuth(config["access_key"], config["access_secret"],
                             config["consumer_key"], config["consumer_secret"]))
query = twitter.search.tweets(q=COMPANY, lang="en", result_type="recent", count="10")

print "Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"])

urllist = list()
content_list = list()

for result in query["statuses"]:
    print "@%s %s" % (result["user"]["screen_name"], result["text"])
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
            content = content.replace("\n", " ")
            if content.strip() is not "":
                content_list.append({"title": result, "article": content})
            break

with open(COMPANY+".json", "w") as js_file:
    json.dump(content_list, js_file)
