__author__ = 'YANG'
import json
import sys

file_name = sys.argv[1]

with open(file_name, 'r') as js_file:
    data = json.load(js_file)
    for item in data:
        print item["title"].encode("UTF-8")
        print "---"
        print item["article"].encode("UTF-8")
        print "=========\n\n"
