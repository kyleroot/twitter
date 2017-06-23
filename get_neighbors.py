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

consumer_key = 'XXXX'
consumer_secret = 'XXXX'
access_token = 'XXXX'
access_token_secret = 'XXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def get_site_handle_pairs(fname):
    with open(fname, 'rb') as f:
            reader = csv.reader(f)
            l = list(reader)
    return [(pair[0], pair[1]) for pair in l if pair]

def get_audiences(handles):
    result = []
    for handle in handles:
        ids = api.followers_ids(handle)
        random_ids = []
        for i in range(120):
            random_ids.append(random.choice(ids))
        result.append((handle, random_ids))
    return result

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("sites", help='path to site list')
    args = argparser.parse_args()
    handles = [pair[1] for pair in get_site_handle_pairs(args.sites)]

    for brand, audience in get_audiences(handles):
        print brand, audience
        print len(audience)
        print
