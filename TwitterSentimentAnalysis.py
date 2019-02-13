import tweepy
from textblob import textblob
import csv
import numpy as np
from keys import *

# Step 1 - Authenticate
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


# where i got the candidates:https://www.nytimes.com/2019/01/04/nyregion/public-advocate-nyc-special-election.html
candidates_names = ['Rafael L. Espinal Jr', 'Daniel O’Donnell', 'Ronald T. Kim','Latrice Walker','Michael A. Blake','Ydanis Rodriguez ','Eric Ulrich','Manny Alicandro','Dawn Smalls','Benjamin Yee','David Eisenbach','Helal A. Sheikh']
#hashtags related to it
name_of_debate ="NYCPublicAdvocate"

since_date = "2019-01-01"
until_date = "2019-02-12"

def get_label(analysis, threshold = 0):
	if analysis.sentiment[0]>threshold:
		return 'Positive'
	else:
		return 'Negative'

#save each Tweet to a CSV file
#and label each one as either 'positive' or 'negative'
#Retrieve Tweets and Save Them
all_polarities = dict()
for candidate in candidates_names:
	this_candidate_polarities = []
	#Get the tweets about the debate and the candidate between the dates
	this_candidate_tweets = api.search(q=[name_of_debate, candidate], count=100, since = since_date, until=until_date)
	#Save the tweets in csv
	with open('%s_tweets.csv' % candidate, 'wb') as this_candidate_file:
		this_candidate_file.write('tweet,sentiment_label\n')
		for tweet in this_candidate_tweets:
			analysis = TextBlob(tweet.text)
			#Get the label corresponding to the sentiment analysis
			this_candidate_polarities.append(analysis.sentiment[0])
			this_candidate_file.write('%s,%s\n' % (tweet.text.encode('utf8'), get_label(analysis)))
	#Save the mean for final results
	all_polarities[candidate] = np.mean(this_candidate_polarities)
 
#Print a Result
sorted_analysis = sorted(all_polarities.items(), key=operator.itemgetter(1), reverse=True)
print 'Mean Sentiment Polarity in descending order :'
for candidate, polarity in sorted_analysis:
	print '%s : %0.3f' % (candidate, polarity)
