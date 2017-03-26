import tweepy
import time
import os
import sys
import json
import argparse

FOLLOWING_DIR = 'following'
MAX_FRIENDS = 100
FRIENDS_OF_FRIENDS_LIMIT = 1000
RESULTS_DIR = "results"
MIN_TWEETS = 500

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

    user = {}
    tweetcount = 0
    max_id = -1
    sinceId = None
    userid.strip()
    fname = userid + ".json"

    if(os.path.exists(os.path.join(RESULTS_DIR, fname))):
        print fname, " exists";
        return

    print userid
    
    user["user"] = api.get_user(id=userid)
    time.sleep(60)
    # print user[userid]
    
    # follower_ids = []
    # for page in tweepy.Cursor(api.followers_ids, screen_name=userid).pages():
    #     follower_ids.extend(page)
        
    #     print len(follower_ids),"followers so far"
    #     if(len(follower_ids) > (min(MAX_FRIENDS, user["user"].followers_count))):
    #         follower_ids = follower_ids[0:MAX_FRIENDS]
    #         print len(follower_ids), "is the new length"
    #         break
    #     time.sleep(60)
        
    # user['follower_ids'] = follower_ids;
    
    tweets = [];
    for page in tweepy.Cursor(api.user_timeline, screen_name=userid).pages():
        tweets.extend(page)
        print "tweets so far",len(tweets)
        
        if(len(tweets) > (min(MIN_TWEETS, user["user"].statuses_count))):
            break;
        
        time.sleep(60)
    
    user["user"] = user["user"]._json
    
    user['tweets'] = []
    
    for tweet in tweets:
        user['tweets'].append(tweet._json)

    with open(os.path.join(RESULTS_DIR, fname), 'w') as f:
        f.write(json.dumps(user, indent=1))

    # print("Downloaded {} tweets, saved to {}".format(len(follower_ids), fname))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--username", required=False, help="User name")
    ap.add_argument("-f", "--file", required=False, help="File with user ids")
    args = vars(ap.parse_args())

    file = args['file']
    
    if(file is not None):
        with open(file, 'r') as f:
            for line in f:
                newline = line.rstrip('\r\n')
                # print newline
                search_twitter_user_to_json(newline)
    
    else:
        userid = args['username']
        search_twitter_user_to_json(userid)
    


