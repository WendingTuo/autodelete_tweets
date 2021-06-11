# autodelete_cc

This program is intended retrieve tweets and likes > 7 days old and delete them.

## Set Up

1. In order to authenticate, you'll need to create a credential file in the program directory using the following details:  
	Filename: `api_secrets.py`  
	Contents:  
	```
		consumer_key = ""  
		consumer_secret = ""  
		access_token = ""  
		access_token_secret = ""  
	```
2. Fill in the variables with the account secrets from your twitter dev instance.
3. Change the `daysAgo` variable to the number of days worth of tweets/favorites you'd like to keep. (Default = 10)
4. Run manually, or set to run as a daily cron job
