import tweepy
from textblob import textblob
import csv
from keys import *

# Step 1 - Authenticate
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#retrievieving tweets
tweets= api.search('')
#save each Tweet to a CSV file
#and label each one as either 'positive' or 'negative'
for tweet in tweets:
    analysis = TextBlob(tweet.text)
    with open('twitterSentimentAnalysis.csv', mode='w') as csv_file:
    fieldnames = ['positive', 'negative']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader(tweet.text)
