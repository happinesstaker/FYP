__author__ = 'Jiajie YANG'

import json
import psycopg2
import os
import FYPsetting

def save_local(content, source, company):
    '''
    This function saves content crawled as local json copy

    argument: content -> list of DB entity
              source -> str (crawler type)
              company -> str
    '''
    if not os.path.isdir("/var/FYP_backup"):
        os.mkdir("/var/FYP_backup")
    with open("/var/FYP_backup/%s.%s.json" % (company, source), "w") as js_file:
        json.dump(content, js_file)

def save_db(content):
    '''
    This function will save raw content to postgresql DB
    '''
    db_setting = FYPsetting.DB_CONFIG
    
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    cur = conn.cursor()
    cur.execute("""PREPARE myplan as INSERT INTO article_table VALUES ($1, $2, $3, $4, $5)""")
    for item in content_list:
        try:
            cur.execute("""execute myplan (%s, %s, %s, %s, %s)""", (item["hash"], item["title"], item["link"], item["source"], item["article"]))
        except:
            print "\n!Identical Item Inserted!\n"
            pass
    conn.commit()
    cur.close()
    
    conn.close()