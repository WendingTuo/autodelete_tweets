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
daysAgo = 360 #!Commenting out to streamline testing #int(input('How far back would you like to retain your tweets?'))

oldestDateToKeep = datetime.now() - timedelta(days=daysAgo)

#* Collect all the tweets we can (Important Fields: tweet.id, tweet.created_at, tweet.favorited, tweet.retweeted)
rawTweets = tw.Cursor(api.user_timeline, id=user_id,).items()

tweetsToDelete = []
for tweet in rawTweets:
    if tweet.created_at < oldestDateToKeep:
        print(tweet.id)
        tweetsToDelete.append(tweet.id)

print(tweetsToDelete)

def deleteTweets(tweetsList):
    for tweet in tweetsList:
        try:
            api.destroy_status(tweet)
            print("Deleted:", tweet)
        except Exception:
            print("Failed to delete:", tweet)


#* Now we'll handle the Favorites
rawFavorites = tw.Cursor(api.favorites, id=user_id).items()
print(rawFavorites)

tweetsToUnfavorite = []
for tweet in rawFavorites:
    if tweet.created_at < oldestDateToKeep:
        print(tweet.id)
        tweetsToUnfavorite.append(tweet.id)

print(tweetsToUnfavorite)

def unfavoriteTweets(tweetsList):
    for tweet in tweetsList:
        try:
            api.destroy_favorite(tweet)
            print("Unfavorited:", tweet)
        except Exception:
            print("Failed to unfavorite:", tweet)

#* This is the main deletion code - Asks for y/n and proceeds to delete or quit based on the answer.
while (res:= input('Do you want to delete ' + str(len(tweetsToDelete)) + ' and unfavorite ' + str(len(tweetsToUnfavorite)) + ' tweets? (y/n): ').lower()) not in {"y", "n"}: pass
if res=='y':
    print("Deleting/Unfavoriting tweets now!")
    deleteTweets(tweetsToDelete)
    unfavoriteTweets(tweetsToUnfavorite)
if res=='n':
    print("Exiting in 3 seconds...")
    time.sleep(3)
sys.exit()