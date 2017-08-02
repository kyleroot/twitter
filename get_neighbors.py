'''

create neighbor data following Culotta et al 2015

usage: replace values for key and token data, then run

$ python get_neighbors.py PATH_TO_SITE_LIST

Source: section 3.2 of Predicting the Demographics of Twitter Users from Website Traffic Data

http://cs.iit.edu/~culotta/pubs/culotta15predicting.pdf

TL;DR
Step 1: get an audience sample of 120 FOLLOWERS for each site
Step 2: for each audience member, get up to 5,000 FRIENDS
Step 3: compute neighbor vectors
Step 4: dimensionality reduction

'''


import tweepy
import argparse
import csv
import random
import logging
import time
import os

logging.basicConfig(filename='get_neighbors.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def get_site_handle_pairs(fname):
    with open(fname, 'rb') as f:
            reader = csv.reader(f)
            l = list(reader)
    return [(pair[0], pair[1]) for pair in l if pair]


def get_brands_followers(handles):
    result = []
    for handle in handles:
        ids = api.followers_ids(handle)
        random_ids = []
        while len(random_ids) != 120:
            choice = random.choice(ids)
            if choice not in random_ids:
                random_ids.append(choice)
        result.append((handle, random_ids))
    return result


def get_followers_friends(brands_followers):
    followers_friends = []
    for brand, followers in brands_followers:
        for id in followers:
            friends_ids = []
            try:
                for friend_id in tweepy.Cursor(api.friends_ids, id=id).items(5000):
                    friends_ids.extend([friend_id])
                    time.sleep(60)
            except tweepy.error.TweepError:
                logger.debug('could not get friends of user %s' % id)
        followers_friends.append((id, friends_ids))
    return followers_friends


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("sites", help='path to site list')
    args = argparser.parse_args()
    handles = [pair[1] for pair in get_site_handle_pairs(args.sites)]
    brands_followers = get_brands_followers(handles)
    followers_friends = get_followers_friends(brands_followers)
