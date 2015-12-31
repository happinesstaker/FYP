# FYP - FLIN1
---
#### Function of modules

*All modules are renamed for clarity*

>crawler_twitter.py execute twitter search and follow external link

>crawler_nyt.py search NY Times Database

>crawler_nasdaq.py search in NASDAQ news

>crawler_google.py use Google news RSS

---
#### UPDATE: Instruction for database (12.28)

To access DB:

`enter http://54.201.171.89/phppgadmin/ in browser`

*ALL User&Pass is **FYP***

To manually crawl data, in AWS VM, run
`python crawling.py`
in FYP folder

*You can also execute each crawler seperately for debugging purpose*

**DO NOT modify code** in VM for purpose of management, only update locally and push to github

---
#### UPDATE: Modules Centralized (12.31)

All modules are well organized and tested already, you can get data with them

**Auto Run:** Add crawling.py to linux scheduler to let it run each hour or so