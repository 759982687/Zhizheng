import tweepy
import csv
import pandas as pd
import sys
import datetime as dt

consumer_key= "PM43l0E6PPK2qNdeAmsKNEz7k"
consumer_secret= "95phoJ00pRX0kXjFmndOlJrPBGHtwQhInNycpcDnOCRDnP50p0"
access_token= "1322032756126224384-qq3Vppy8tCebrdToefikIXlMfAQeuq"
access_token_secret= "oFmko6FXJi36XbkUAYxeafOxX595nOGMAeuUYBlIXN555"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# Search word/hashtag value 
search_words = "e"

# search start date value. the search will start from this date to the current date.
StartDate = "2020-01-01"
EndDate = "2020-11-11"
search_loc = "San Diego"

# getting the search word/hashtag and date range from user
#search_words = input("Enter the search words you want the tweets to be downloaded for: ")
#StartDate = input("Enter the start date in this format yyyy-mm-dd: ")
#EndDate = input("Enter the end date in this format yyyy-mm-dd: ")
#search_loc = input("Enter the location you want the tweets to be from ")
limit = 1000

# Open/Create a file to append data
csvFile = open(search_words+'.csv', 'a')

#Use csv Writer
csvWriter = csv.writer(csvFile)

#for tweet in tweepy.Cursor(api.search,q=search_words,count=50,lang="en",since=StartDate,till = EndDate, loc=search_loc,limit = limit,tweet_mode='extended').items():
#    print (tweet.created_at, tweet.full_text)
#    csvWriter.writerow([tweet.created_at, tweet.full_text.encode('utf-8')])
#open("tweets.txt", 'a') as tf:

for tweet in tweepy.Cursor(api.search,q=search_words,count=50,lang="en").items():
    print (tweet.created_at, tweet.text)
    
    csvWriter.writerow([tweet.created_at, tweet.user,tweet.text.encode("unicode_escape")])
    #tf.write()

print ("Scraping finished and saved to "+search_words+".csv")
#sys.exit()search_words