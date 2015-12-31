# FYP

Crawler.py execute twitter search

Crawler2.py search NY Times Database

Crawler3.py search in NASDAQ

Crawler4.py use Google news RSS

UPDATE: Instruction for database

## Note that currently only crawler.py inserts into DB, I'll write a central module for DB insertion and combine all crawlers soon.

# FYP

##

###Function of modules

*All modules are renamed for clarity*

>crawler_twitter.py execute twitter search and follow external link

>crawler_nyt.py search NY Times Database

>crawler_nasdaq.py search in NASDAQ news

>crawler_google.py use Google news RSS


###UPDATE: Instruction for database

To access DB:

`enter http://54.201.171.89/phppgadmin/ in browser`

*ALL User&Pass is **FYP***

In AWS VM, run

`python crawling.py`
in FYP folder

**DO NOT** modify code in VM for purpose of management, only update locally and push to github, VM will only be used to execute code

