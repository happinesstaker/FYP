from linkedin import linkedin
import FYPsetting
import json
import urllib2
import psycopg2
import os


def write_related_company(main_company):

    config = FYPsetting.LINKEDIN_CONFIG
    
    CONSUMER_KEY = config["customer_id"]     # This is api_key
    CONSUMER_SECRET = config["customer_secret"]   # This is secret_key
    USER_TOKEN = config["oauth_token"]   # This is oauth_token
    USER_SECRET = config["oauth_secret"]   # This is oauth_secret
    RETURN_URL = "http://54.201.171.89/"
    
    # open application
    authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                                        USER_TOKEN, USER_SECRET, 
                                                        RETURN_URL)
    
    application = linkedin.LinkedInApplication(authentication)
    
    # query for similar companies
    #main_company = raw_input("Specify the main target company you want: ")
    result = application.search_company(selectors=[{'companies': ['name', 'universal-name']}], params={'keywords': main_company})
    
    companies = result["companies"]["values"]
    company_list = [item["universalName"] for item in companies]
    company_dict = dict()
    
    ''' For User Interactive purpose
    for index, value in enumerate(company_list):
        print str(index+1)+". "+value
    
    # generate desired company list
    desired_index = raw_input("Select a list of additional company you want (eg: 136): ")
    
    
    additional_company_list = list()
    
    for num in desired_index:
        int_num = int(num)
        if int_num>0 and int_num<=len(company_list):
            additional_company_list.append(company_list[int_num-1])
    '''
    additional_company_list = company_list[:3]
    
    # translate universal company name to nasdaq symbol
    company_codes = list()
    
    for raw_name in additional_company_list:
        url = "http://d.yimg.com/aq/autoc?query=%s&region=US&lang=en-US" % raw_name
        conn = urllib2.urlopen(url)
        candidate_codes = json.loads(conn.read())
        
        for candidate in candidate_codes["ResultSet"]["Result"]:
            if candidate["exchDisp"] == "NASDAQ":
                company_codes.append(candidate["symbol"])
                company_dict[raw_name] = candidate["symbol"]
                break
        else:
            company_dict[raw_name] = ""
    
            
    final_output = {"company_code":company_codes,
                    "all_companies":additional_company_list}
                    
    with open("%s/target_companies.json" % os.path.dirname(os.path.realpath(__file__)),"w") as outfile:
        json.dump(final_output, outfile)
        #print "target_companies.json updated..."
        
    # DB operation
    db_setting = FYPsetting.DB_CONFIG
    
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (db_setting["dbname"], db_setting["user"], db_setting["password"], db_setting["host"], db_setting["port"]))
    except:
        print "Cannot Connect Database!"
        exit(-1)
    
    cur = conn.cursor()
    conn.commit()
    
    for item in company_dict:
        try:  
            cur.execute("""INSERT INTO company_table VALUES (%s, %s)""", (item, company_dict[item]))
        except psycopg2.IntegrityError as err:
            conn.rollback()
            continue
        else:
            conn.commit()
    
    cur.close()
    conn.close()
    
    return os.path.dirname(os.path.realpath(__file__))
