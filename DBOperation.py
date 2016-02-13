__author__ = 'Jiajie YANG, Sirui XIE'

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
    cur.execute("""PREPARE myplan as INSERT INTO article_table VALUES ($1, $2, $3, $4, $5, $6)""")

    for item in content:
        try:
            
            cur.execute("""execute myplan (%s, %s, %s, %s, %s, %s)""", (item["hash"], item["title"], item["link"], item["source"], item["article"], item["date"]))
        except psycopg2.IntegrityError as err:
            conn.rollback()
            continue
        else:
            conn.commit()

        
    cur.close()
    conn.close()

def query_db(date):
    '''
    This function queries raw content from postgresql DB
    with date in the format of "%04d%02d%02d"
    '''
    db_setting = FYPsetting.DB_CONFIG
    title_list = []

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    cur = conn.cursor()
    # try to handle the null exception
    try:
        cur.execute("""SELECT title FROM article_table WHERE date = (%s);""", date)
    except:
        print "Notice! There is no article in %s", date

    title_list.extend(cur.fetchall())

    cur.close()
    conn.close()

    return title_list


