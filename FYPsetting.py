#This is the main setting file for this FYP project

QUERY_PAGE = 10

#Length of char are limited in DB
TITLE_LEN_LIMIT = 299
LINK_LEN_LIMIT = 299
CONTENT_LEN_LIMIT = 5999

DB_CONFIG = {"dbname":"Articles",
             "user":"FYP",
             "password":"FYP",
             "host":"localhost",
             "port":"5432"}

TWITTER_CONFIG = {"access_key": "3780616332-PArbYD6xifva5Zo9oTUqg6yJlPwYa9WdR53Tdlk",
                  "access_secret": "ccXRQorrexkTS3xpRYHJobT11eGA3i4MB6Bj7WezRvevO",
                  "consumer_key": "RctxsgdWyhHpfNDIeUPAxKJ5f",
                  "consumer_secret": "Lx4GAVULXCsFlHE50sw3m8Ca6w6IDK5hLkBCSCL7HSVtyQiJh2",
                  "company":"cisco"}
                  
NYT_CONFIG = {"API_key":'dafd1e77c5a943648589c495de8e9d73:6:72720402',
              "begin_date":"20100101",
              "company":"cisco"}
              
NASDAQ_CONFIG = {"company": "csco"} #cisco

GOOGLE_CONFIG = {"company": "cisco"}

LINKEDIN_CONFIG = {"customer_id":"75uyw84y65lswo",
                   "customer_secret":"aXurvuFrYEca1oaR",
                   "oauth_token":"6f84134e-845b-4a82-aaa5-0033c187b410",
                   "oauth_secret":"5f282dbb-1922-4b6e-85f4-5d493e0bd92a"}