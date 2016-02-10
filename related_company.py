from linkedin import linkedin

config = FYPsetting.LINKEDIN_CONFIG

CONSUMER_KEY = config["customer_id"]     # This is api_key
CONSUMER_SECRET = config["customer_secret"]   # This is secret_key

USER_TOKEN = config["oauth_token"]   # This is oauth_token
USER_SECRET = config["oauth_secret"]   # This is oauth_secret

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                                      USER_TOKEN, USER_SECRET, 
                                                      RETURN_URL)

# Pass it in to the app...

application = linkedin.LinkedInApplication(authentication)

# Use the app....

application.get_profile()