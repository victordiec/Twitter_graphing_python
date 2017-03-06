import tweepy
import time
import os
import sys
import json
import argparse

FOLLOWING_DIR = 'following'
MAX_FRIENDS = 1000
FRIENDS_OF_FRIENDS_LIMIT = 1000
RESULTS_DIR = "results"

if not os.path.exists(FOLLOWING_DIR):
    os.mkdir(FOLLOWING_DIR)

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
CONSUMER_KEY = os.environ['APP_KEY']
CONSUMER_SECRET = os.environ['APP_SECRET']

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
ACCESS_TOKEN = os.environ['OAUTH_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

# User is the data model for a user profile
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse

# Process a single status
def search_twitter_user_to_json(userid):

    d = {}
    tweetcount = 0
    max_id = -1
    sinceId = None
    fname = "followers_" + userid + ".json"

    print userid
    
    follower_ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=userid).pages():
        follower_ids.extend(page)
        time.sleep(60)
    
    print len(follower_ids)
    
    followers = {}
    for follower_id in follower_ids:
        follower = api.get_user(id=follower_id)
        # print follower._json
        # followers.append(follower)
        followers[follower_id] = follower._json

    with open(os.path.join(RESULTS_DIR, fname), 'w') as f:
        f.write(json.dumps(followers, indent=1))

    print("Downloaded {} tweets, saved to {}".format(len(follower_ids), fname))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--username", required=True, help="User name")
    # ap.add_argument("-c", "--count", required=True, type=int, help="Number of tweets per page")
    # ap.add_argument("-m", "--max", required=True, type=int, help="Maximum number of tweets")
    args = vars(ap.parse_args())

    userid = args['username']
    # count = int(args['count'])
    # maxtweets = int(args['max'])

    search_twitter_user_to_json(userid)
