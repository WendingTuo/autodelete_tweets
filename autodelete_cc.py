import os
import tweepy as tw
import pandas as pd

#* Import the api_secrets variables
from api_secrets import *

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

#* Collect the tweets

tweets = tw.API.statuses_lookup()

print(tweets)