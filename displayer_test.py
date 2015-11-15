__author__ = 'YANG'
import json

file_name = 'cisco.GOOGLE.json'

with open(file_name, 'r') as js_file:
    data = json.load(js_file)
    for item in data:
        print item["title"]
        print "---"
        print unicode(item["article"])
        print "=========\n\n"