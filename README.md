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

*ALL User&Pass is FYP*

To manually crawl data, in AWS VM, run
`python crawling.py`
in FYP folder

*You can also execute each crawler seperately for debugging purpose*

**DO NOT modify code** in VM for purpose of management, only update locally and push to github

---
#### UPDATE: Modules Centralized (12.31)

All modules are well organized and tested already, you can get data with them

**Auto Run:** Add crawling.py to linux scheduler to let it run each hour or so

---
#### UPDATE: Crawler Data Modification (2.9)

Pre-process Title from Twitter to let it be more readabale

Add Attribute: Data Collection Time

---
#### UPDATE: Related Company List Feature Added (2.11)

*Run related_company to update the list of related companies, which is saved in target_companies.json*

Query LinkedIn API for related companies like subsidiary or holding company

Rewrite crawler to support multi-company crawling

---
#### UPDATE: UMBC Comparasion Added (2.13)

Query titles from database for *w* days from today to compare, return a list of candidates

*LSA is currently omitted*

*The specific rules for path distance weighing is also omitted*

---
#### UPDARTE: UMBC with LSA finished (3.27)

LSA is implemented as stated in the paper, WINDOW_SIZE is set to 4.

DIMENSION for SVD is set to 300, which is empirically established by LSA researchers.

*Need to design corpus_table to store corpus documents and the precalculated lsa matrix*


