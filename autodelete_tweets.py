# Import modules
import os
import sys
import time
import tweepy as tw
from datetime import datetime, timedelta
import argparse
from pushover import init, Client

# Import the api_secrets variables
from api_secrets import *

# Import Twitter authentication information from api_secrets.py
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
user = api.me()
user_id = user.id

# Initialize Pushover using authentication information from api_secrets.py
pushoverClient = Client(pushover_user_key, api_token=pushover_api_token)

#* Set how far back you'd like to retain tweets
daysAgo = 10
oldestDateToKeep = datetime.now() - timedelta(days=daysAgo)

#* Import the CLI arguments, if any
def cliSetup():
    cliParser = argparse.ArgumentParser(description="Deletes and unfavorites tweets more than X days old.")
    cliParser.add_argument("-c", "--confirm", help="'y' confirms the deletion on launch, 'n' will just print the lists of collected tweets")
    args = cliParser.parse_args()
    return args.confirm

cliConfirm = cliSetup()

#* Collect all the tweets we can (Important Fields: tweet.id, tweet.created_at, tweet.favorited, tweet.retweeted)
tweetsToDelete = []
rawTweets = tw.Cursor(api.user_timeline, id=user_id).items(500)
for tweet in rawTweets:
    if tweet.created_at < oldestDateToKeep:
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
tweetsToUnfavorite = []
rawFavorites = tw.Cursor(api.favorites).items(600)

for tweet in rawFavorites:
    if tweet.created_at < oldestDateToKeep:
        tweetsToUnfavorite.append(tweet.id)

print(tweetsToUnfavorite)

def unfavoriteTweets(tweetsList):
    for tweet in tweetsList:
        try:
            api.destroy_favorite(tweet)
            print("Unfavorited:", tweet)
        except Exception:
            print("Failed to unfavorite:", tweet)

#* This is the main deletion code - Asks for y/n via CLI and proceeds to delete or quit based on the answer.
if cliConfirm == 'y':
    pushoverClient.send_message("Deleting " + str(len(tweetsToDelete)) + " and unfavoriting " + str(len(tweetsToUnfavorite)) + " tweets now!")
    deleteTweets(tweetsToDelete)
    unfavoriteTweets(tweetsToUnfavorite)
    pushoverClient.send_message("Deleted " + str(len(tweetsToDelete)) + " and unfavorited " + str(len(tweetsToUnfavorite)) + " tweets!", title="Autodelete Complete")
elif cliConfirm=='n':
    print("No deletion requested - To delete, change your cli argument to '-c y'.")
    pushoverClient.send_message("Collected " + str(len(tweetsToDelete)) + " tweets to delete and " + str(len(tweetsToUnfavorite)) + " to unfavorite!", title="Autodelete Incomplete")
else:
    while (res:= input('Do you want to delete ' + str(len(tweetsToDelete)) + ' and unfavorite ' + str(len(tweetsToUnfavorite)) + ' tweets? (y/n): ').lower()) not in {"y", "n"}: pass
    if res=='y':
        print("Deleting/Unfavoriting tweets now!")
        deleteTweets(tweetsToDelete)
        unfavoriteTweets(tweetsToUnfavorite)
    if res=='n':
        print("Deletion cancelled!")

print("Exiting in 3 seconds...")
time.sleep(3)
sys.exit()
