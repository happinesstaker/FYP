__author__ = 'Jiajie YANG, Sirui XIE'

import json
import psycopg2
import os
import FYPsetting
import datetime


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

            cur.execute("""execute myplan (%s, %s, %s, %s, %s, %s, %s)""", (item["hash"], (item["title"].encode('latin-1', 'ignore'))[:FYPsetting.TITLE_LEN_LIMIT], item["link"][:FYPsetting.LINK_LEN_LIMIT], item["source"], (item["article"].encode('latin-1', 'ignore'))[:FYPsetting.CONTENT_LEN_LIMIT], item["date"], item["target"][:FYPsetting.TARGET_LEN_LIMIT]))
        except psycopg2.IntegrityError as err:
            conn.rollback()
            continue
        else:
            conn.commit()


    cur.close()
    conn.close()


def query_title(date):
    '''
    This function queries raw title from postgresql DB
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


def query_corpus():
    '''
    This function queries corpus documents from postgresql DB (select all)
    :return: a list of documents
    '''

    db_setting = FYPsetting.DB_CONFIG
    doc_list = []

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    cur = conn.cursor()
    # try to handle the null exception
    try:
        cur.execute("""SELECT content FROM corpus_table;""")
    except:
        print "Notice! Corpus not found!"

    doc_list.extend(cur.fetchall())

    cur.close()
    conn.close()

    return doc_list


def query_lsa():
    '''
    This function queries lsa matrix from postgresql DB (select all)
    :return: a list of documents
    '''

    db_setting = FYPsetting.DB_CONFIG
    matrix = []

    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)

    cur = conn.cursor()
    # try to handle the null exception
    try:
        cur.execute("""SELECT matrix FROM corpus_table;""")
    except:
        print "Notice! Corpus not found!"

    matrix.extend(cur.fetchall())

    cur.close()
    conn.close()

    return matrix

