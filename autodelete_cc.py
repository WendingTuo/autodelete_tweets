# Import modules
import os
import sys
import time
import tweepy as tw
from datetime import datetime, timedelta

# Import the api_secrets variables
from api_secrets import *

# Import authentication information
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
user = api.me()
user_id = user.id

#* Set how far back you'd like to retain tweets
daysAgo = 110 #!Commenting out to streamline testing #int(input('How far back would you like to retain your tweets?'))

oldestDateToKeep = datetime.now() - timedelta(days=daysAgo)

#* Collect all the tweets we can (Important Fields: tweet.id, tweet.created_at, tweet.favorited, tweet.retweeted)
rawTweets = api.user_timeline(user_id, count = 3200)

tweetsToDelete = []
for tweet in rawTweets:
    if tweet.created_at < oldestDateToKeep:
        print(tweet.id)
        tweetsToDelete.append(tweet.id)
        
tweetsToUnfavorite = []
for tweet in rawTweets:
    if tweet.created_at < oldestDateToKeep and tweet.favorited is True:
        print(tweet.id)
        tweetsToUnfavorite.append(tweet.id)

print(tweetsToDelete)
print(tweetsToUnfavorite)

def deleteTweets(tweetsList):
    for tweet in tweetsList:
        try:
            api.destroy_status(tweet)
            print("Deleted:", tweet)
        except Exception:
            print("Failed to delete:", tweet)

def unfavoriteTweets(tweetsList):
    for tweet in tweetsList:
        try:
            api.destroy_favorite(tweet)
            print("Deleted:", tweet)
        except Exception:
            print("Failed to delete:", tweet)

while (res:= input('Do you want to delete ' + str(len(tweetsToDelete)) + ' and unfavorite ' + str(len(tweetsToUnfavorite)) + ' tweets? (y/n): ').lower()) not in {"y", "n"}: pass
if res=='y':
    print("Deleting/Unfavoriting tweets now!")
    deleteTweets(tweetsToDelete)
    unfavoriteTweets(tweetsToUnfavorite)
if res=='n':
    print("Exiting in 3 seconds...")
    time.sleep(3)
sys.exit()