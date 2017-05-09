#Python3
import os
import array
import argparse
import random
from statistics import mean
from statistics import variance
from collections import Counter

from timezonefinder import TimezoneFinder
tf = TimezoneFinder()

import json
from pprint import pprint

RESULTS_DIR = "statsResults"


# Information : https://dev.twitter.com/overview/api/tweets

def get_stats(twitterAccount):
    
    # pprint(twitterAccount)
    
    #Setting up object to print 
    stats = {}
    stats["lists"] = []
    stats["stats"] = {}
    stats["stats"]["fav"] = {}
    stats["stats"]["geo_enabled"] = {}
    stats["stats"]["quoted"] = {}
    stats["stats"]["symbol"] = {}
    stats["stats"]["hash"] = {}
    stats["stats"]["url"] = {}
    stats["stats"]["url_possibly_sensitive"] = {}
    stats["stats"]["retweet"] = {}
    stats["stats"]["protected"] = {}
    
    stats["stats"]["time_quarter_frequency"] = {}
    stats["stats"]["timezone_freq"] = {}
    
    stats["quote_list"] = []
    stats["is_fav_list"] = []
    stats["retweet_list"] = []
    stats["geo_enabled_list"] = []
    stats["hashtag_list"] = []
    stats["symbol_list"] = []
    stats["url_list"] = []
    stats["possibly_sensitive_list"] = []
    stats["protected"] = []
    
    stats["time_quarter"] = []
    stats["timezone_list"] = []
    
    # Fake the protection by making a string of 1s and 0s signifiying whether they were protected at the point in time of the tweet
    # We'll fake coordinate data, make sure they are all in the same time zone
    # We just assign a timezone, and we'll have some users with some fluctuating time zones
    
    # Frequency for timezones as in location
    # Frequency for when tweet times
    
    
    # Divide the day into quarters
    #0  00:00-5:59
    #1  06:00-11:59
    #2  12:00-17:59
    #3  18:00-23:59
    

    
    
    # Location based off timezone frequency...
    # stats["location_list"] = {}
    
    # print(len(twitterAccount["tweets"]))
    
    # for each tweet in the twitter account
    
    inRandTimeZone = False
    mainTimeZone = random.randint(0, 418)
    randomTimeZone = random.randint(0, 418)
    randomTimeZoneDur = random.randint(20, 100)
    
    for tweet in twitterAccount["tweets"]:

        try:
            stats["quote_list"].append(1 if tweet["is_quote_status"] == True else 0)
            stats["is_fav_list"].append(1 if tweet["favorite_count"] > 0 else 0)
            stats["retweet_list"].append(1 if tweet["retweet_count"] > 0 else 0)
            stats["geo_enabled_list"].append(1 if tweet["coordinates"] is not None else 0)
            stats["hashtag_list"].append(1 if len(tweet["entities"]["hashtags"]) > 0  else 0)
            stats["symbol_list"].append(1 if len(tweet["entities"]["symbols"]) > 0  else 0)
            stats["url_list"].append(1 if len(tweet["entities"]["urls"]) > 0  else 0)
            stats["possibly_sensitive_list"].append(1 if ('possibly_sensitive' in tweet.keys()) and (tweet["possibly_sensitive"] == True) else 0)
            stats["protected"].append(random.randint(0,1))
            
            timezone = None
            
            #If we have not gone to the random time zone for a certain duration, we can check if we can still switch
            #We have a 7% chance of changing timezones
            if(random.randint(0,100) <= 7 and not inRandTimeZone and randomTimeZoneDur > 0):
                inRandTimeZone = True
                timezone = randomTimeZone
                randomTimeZoneDur = randomTimeZoneDur - 1
            
            #Else we have to check if it's already in the random time zone
            elif(inRandTimeZone):
                randomTimeZoneDur = randomTimeZoneDur - 1
                timezone = randomTimeZone
                inRandTimeZone = True if randomTimeZoneDur > 0 else False
                
            #Otherwise it's in the maintimezone
            else:
                timezone = mainTimeZone
            
            stats["timezone_list"].append(timezone)    
            
            # Introducting Noise
            # Find Mean and Variance
            # Generate a pdf function, cdf gives the P(X > Y)
            # Send general formula 
            
            # Generate gaussian signal, multiply variance by number between 1 and 2
            # Add these values on top of original signal
            # Noise will be Gaussian
            # We can add to a binary signal (We have to check if it goes even or odd)
            
            
            time = tweet["created_at"][10:19];
            
            if (0 <= float(time[:3]) <= 5):     stats["time_quarter"].append(0) 
            if (6 <= float(time[:3]) <= 11) :   stats["time_quarter"].append(1) 
            if (12 <= float(time[:3]) <= 17):   stats["time_quarter"].append(2) 
            if (18 <= float(time[:3]) <= 23):   stats["time_quarter"].append(3) 
                
        except KeyError:
            print("Error")
            pprint(tweet)
            return
        
    
    stats["stats"]["fav"]["mean"] = mean(stats["is_fav_list"])
    stats["stats"]["fav"]["variance"] = variance(stats["is_fav_list"])
    
    stats["stats"]["geo_enabled"]["mean"] = mean(stats["geo_enabled_list"])
    stats["stats"]["geo_enabled"]["variance"] = variance(stats["geo_enabled_list"])
    
    stats["stats"]["quoted"]["mean"] = mean(stats["quote_list"])
    stats["stats"]["quoted"]["variance"] = variance(stats["quote_list"])
    
    stats["stats"]["symbol"]["mean"] = mean(stats["symbol_list"])
    stats["stats"]["symbol"]["variance"] = variance(stats["symbol_list"])
    
    stats["stats"]["hash"]["mean"] = mean(stats["hashtag_list"])
    stats["stats"]["hash"]["variance"] = variance(stats["hashtag_list"])
    
    stats["stats"]["url"]["mean"] = mean(stats["url_list"])
    stats["stats"]["url"]["variance"] = variance(stats["url_list"])
    
    stats["stats"]["url_possibly_sensitive"]["mean"] = mean(stats["possibly_sensitive_list"])
    stats["stats"]["url_possibly_sensitive"]["variance"] = variance(stats["possibly_sensitive_list"])
    
    stats["stats"]["retweet"]["mean"] = mean(stats["retweet_list"])
    stats["stats"]["retweet"]["variance"] = variance(stats["retweet_list"])
    
    stats["stats"]["protected"]["mean"] = mean(stats["protected"])
    stats["stats"]["protected"]["variance"] = variance(stats["protected"])
    
    stats["stats"]["time_quarter_frequency"]["0"] = stats["time_quarter"].count(0)/len(stats["time_quarter"])
    stats["stats"]["time_quarter_frequency"]["1"] = stats["time_quarter"].count(1)/len(stats["time_quarter"])
    stats["stats"]["time_quarter_frequency"]["2"] = stats["time_quarter"].count(2)/len(stats["time_quarter"])
    stats["stats"]["time_quarter_frequency"]["3"] = stats["time_quarter"].count(3)/len(stats["time_quarter"])
    
    for i in range(0, 418):
        stats["stats"]["timezone_freq"][i] = stats["timezone_list"].count(i)/len(stats["timezone_list"])
    
    # pprint(stats["stats"])
    with open(os.path.join(RESULTS_DIR, "stats" + twitterAccount["user"]["screen_name"]) + ".json", 'w') as f:
        f.write(json.dumps(stats, sort_keys=True, indent=1))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=False, help="JSON file containing user's tweets")
    ap.add_argument("-d", "--dir", required=False, help="Directory containing Json files")
    args = vars(ap.parse_args())

    file = args['file']
    dir = args['dir']
    
    if(dir is not None):
        dirFiles = os.listdir(dir)
        for file in dirFiles:
            try:
                with open(os.path.join(dir,file)) as data_file:    
                    twitterAccount = json.load(data_file)
                    get_stats(twitterAccount)
            except Exception as e:
                print(str(e))
                print("Problem file:" + os.path.join(dir,file))
            
    elif(file is not None):
        with open(file) as data_file:    
            twitterAccount = json.load(data_file)
            get_stats(twitterAccount)
            
            
    
