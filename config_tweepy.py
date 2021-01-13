import tweepy
from secrets import *
from os import environ
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

def create_api():
    if "key" in globals():
        consumer_key = key[0]
        consumer_secret = key[1]
        access_token = key[2]
        access_token_secret = key[3]
    else:
        consumer_key = environ['CONSUMER_KEY']
        consumer_secret = environ['CONSUMER_SECRET']
        access_token = environ['ACCESS_KEY']
        access_token_secret = environ['ACCESS_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        logging.info("API created")
    except Exception as e:
        logging.error("Error creating API", exc_info=True)
        raise e
    
    return api