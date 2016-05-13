__author__ = 'Jiajie YANG, Sirui XIE'

import json
import psycopg2
import os
import FYPsetting
import datetime
from datetime import date, timedelta


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


def save_corpus(content):

    if not os.path.isdir("/var/FYP_backup"):
        os.mkdir("/var/FYP_backup")
    with open("/var/FYP_backup/LSA_corpus", "a") as corpus_file:
        corpus_file.write(content)
        corpus_file.write("\n")
        corpus_file.write(FYPsetting.CORPUS_DELIM)


def clean_db(day_offset):
    '''
    Clean old articles to maintain a reasonable DB size

    argument: day_offset -> day before to clean

    '''

    now = datetime.datetime.now()
    past = now - datetime.timedelta(hours=(24*day_offset))
    date_filter_str = "%04d%02d%02d" % (past.year, past.month, past.day)

    db_setting = FYPsetting.DB_CONFIG

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    cur = conn.cursor()
    cur.execute("""DELETE FROM article_table WHERE date<=%s""", (date_filter_str,))
    conn.commit()
    cur.close()
    conn.close()


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

    conn.set_client_encoding('LATIN1')
    cur = conn.cursor()
    cur.execute("""PREPARE myplan as INSERT INTO article_table VALUES ($1, $2, $3, $4, $5, $6, $7)""")

    for item in content:

        #save_corpus(item["article"].encode('latin-1', 'ignore'))

        try:

            cur.execute("""execute myplan (%s, %s, %s, %s, %s, %s, %s)""", (item["hash"], (item["title"].encode('latin-1', 'ignore'))[:FYPsetting.TITLE_LEN_LIMIT], item["link"][:FYPsetting.LINK_LEN_LIMIT], item["source"], (item["article"].encode('latin-1', 'ignore'))[:FYPsetting.CONTENT_LEN_LIMIT], item["date"], item["target"][:FYPsetting.TARGET_LEN_LIMIT]))
        except psycopg2.IntegrityError as err:
            conn.rollback()
            continue
        else:
            conn.commit()


    cur.close()
    conn.close()


def save_db_selected(content):
    '''
    This function will save raw content to postgresql DB
    '''
    db_setting = FYPsetting.DB_CONFIG

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    conn.set_client_encoding('LATIN1')
    cur = conn.cursor()
    cur.execute("""PREPARE myplan as INSERT INTO selected_article_table VALUES ($1, $2, $3, $4, $5, $6, $7)""")

    for item in content:

        #save_corpus(item["article"].encode('latin-1', 'ignore'))

        try:
            cur.execute("""execute myplan (%s, %s, %s, %s, %s, %s, %s)""", (item["hash"], (item["title"])[:FYPsetting.TITLE_LEN_LIMIT], item["link"][:FYPsetting.LINK_LEN_LIMIT], item["source"], (item["article"])[:FYPsetting.CONTENT_LEN_LIMIT], item["date"], item["target"][:FYPsetting.TARGET_LEN_LIMIT]))
        except psycopg2.IntegrityError as err:
            conn.rollback()
            continue
        else:
            conn.commit()


    cur.close()
    conn.close()


def query_articles(date, target):
    '''
    This function queries raw title from postgresql DB
    with date in the format of "%04d%02d%02d"
    '''
    db_setting = FYPsetting.DB_CONFIG
    content_list = list()

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    cur = conn.cursor()
    # try to handle the null exception
    try:
        cur.execute("""SELECT * FROM article_table WHERE date = '%s' AND target = '%s'""" % (str(date), target))
    except:
        print "Notice! There is no article in ", date


    #title_list.extend(cur.fetchall())
    item_list = cur.fetchall()
    '''
    for item in item_list:
        content_list.append({"title": item[1],
                        "article": item[4],
                        "link": item[2],
                        "source": item[3],
                        "target": item[6],
                        "date": item[5],
                        "hash":item[0]})
    '''
    cur.close()
    conn.close()

    #save_db_selected(content_list)
    return item_list

def query_chosen(date, target):
    '''
    This function queries raw title from postgresql DB
    with date in the format of "%04d%02d%02d"
    '''
    db_setting = FYPsetting.DB_CONFIG
    content_list = list()

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    cur = conn.cursor()
    # try to handle the null exception
    try:
        cur.execute("""SELECT * FROM selected_article_table WHERE date = '%s' AND target = '%s'""" % (str(date), target))
    except:
        print "Notice! There is no article in ", date


    #title_list.extend(cur.fetchall())
    item_list = cur.fetchall()
    '''
    for item in item_list:
        content_list.append({"title": item[1],
                        "article": item[4],
                        "link": item[2],
                        "source": item[3],
                        "target": item[6],
                        "date": item[5],
                        "hash":item[0]})
    '''
    cur.close()
    conn.close()

    #save_db_selected(content_list)
    print "done"
    return item_list

def query_by_hash(hash):
    '''
    This function queries raw title from postgresql DB
    with date in the format of "%04d%02d%02d"
    '''
    db_setting = FYPsetting.DB_CONFIG

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    cur = conn.cursor()
    # try to handle the null exception
    try:
        cur.execute("""SELECT * FROM article_table WHERE title_hash = '%s'""" % hash)
    except:
        print "Notice! There is no article in ", date


    #title_list.extend(cur.fetchall())
    item_list = cur.fetchall()
    print item_list
    item= item_list[0]
    '''
    for item in item_list:
        print item[1]
    '''

    cur.close()
    conn.close()

    #save_db_selected(content_list)
    return item

def update_selection(chosen_list, date, target):
    db_setting = FYPsetting.DB_CONFIG

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    conn.set_client_encoding('LATIN1')
    cur = conn.cursor()
    for i in range(FYPsetting.COMPARING_DATES):
        cur.execute("DELETE FROM selected_article_table WHERE date='%s' AND target='%s';" % (str(date-i), target))

    cur.execute("""PREPARE myplan as INSERT INTO selected_article_table VALUES ($1, $2, $3, $4, $5, $6, $7)""")

    for item in chosen_list:

        try:

            cur.execute("""execute myplan (%s, %s, %s, %s, %s, %s, %s)""", (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
        except psycopg2.IntegrityError as err:
            conn.rollback()
            continue
        else:
            conn.commit()


    cur.close()
    conn.close()


if __name__ == '__main__':
    db_setting = FYPsetting.DB_CONFIG

    item1 = query_by_hash('1f761fdd3da10125a175d3348ca77156ad61621120b3c95582ad79f4')
    item2 = query_by_hash('34008dbac97cdfa7c9ef32ea0fdfd8c99ec1c0247d29c4e41ac94940')
    print item1
    print item2
