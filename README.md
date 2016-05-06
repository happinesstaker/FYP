# FYP - FLIN1

#### System Requirement
Language: Python 2.7

Third-party Library:

Crawler: BoilerPipe; feedparser; twitter; oauth2

Model:  nltk; nltk.wordnet; numpy (with OpenBlas linkage);scipy; scipy.sparse; sklearn; gensim

File Format: JSON

---
#### Function of modules

*All modules are renamed for clarity*

>crawler_twitter.py execute twitter search and follow external link, use API & OAuth

>crawler_nyt.py search NY Times Database, use API by NYT

>crawler_nasdaq.py search in NASDAQ news, use BeautifulSoup to extract webpage elements

>crawler_google.py use Google news RSS, use RSS URL

---
#### Instruction for crawler & DB

To access DB:

`enter http://[DB Server IP]/phppgadmin/ in browser`

*ALL User&Pass is FYP*

To run crawler:

in AWS VM, run
`python crawling.py`
in FYP folder

*You can also execute each crawler seperately for debugging purpose*

**Auto Run:** Add crawling.py to linux crontab to let it run each hour or so

---

### Instruction for Similarity Scoring and Selection

All similarity measurements are in Python Package `similarity_scoring`

Run `python selection.py` for article selection. Threshold and parameters are all set in `FYPSetting.py`.

`umbc_scoring.py` is for title comparison, the return value would be in range [0,1], `lsa_matrix.py` and `wordnet_boosting.py` are two component models.

`kld_scoring.py` is for body comparison. It returns a tuple with the first element from *doc1* to *doc2* and the second is for backward. They both in range [0, inf). *(from our observation, it never exceeds 50)*

`tfcos_socring.py` is for evaluation comparison.

Corpus file named `LSA_corpus` was downloaded from [UMBC Corpus](http://ebiquity.umbc.edu/resource/html/id/351).

*Notice: The larger the corpus used, the more accurate the result would be*

Files in the package `semantic` are some utilities for `umbc_scoring`

---

### Instruction for evaluation
Run `python evaluate.py [test size]`

To change corpus for evaluate, modify in GLOBAL setting in the script.


