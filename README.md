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

>Crawler.py execute twitter search

>Crawler2.py search NY Times Database

>Crawler3.py search in NASDAQ

>Crawler4.py use Google news RSS


###UPDATE: Instruction for database

*Note that currently only crawler.py inserts into DB, I'll write a central module for DB insertion and combine all crawlers soon.*

To access DB:

`enter http://54.201.171.89/phppgadmin/ in browser`

*ALL User&Pass is **FYP***

In AWS VM, run

`python crawler.py`
in FYP folder

currently 10 twitter results will be added to DB once a time

**DO NOT** modify code in VM for purpose of management, only update locally and push to github, VM will only be used to execute code

