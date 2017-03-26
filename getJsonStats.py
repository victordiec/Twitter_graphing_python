import argparse

from timezonefinder import TimezoneFinder
tf = TimezoneFinder()

import json
from pprint import pprint

def get_stats(twitterAccount):
    
    pprint(twitterAccount)
    
    #Setting up object to print 
    stats = {}
    stats["lists"] = []
    stats["stats"] = []
    stats["stats"]["fav"] = {}
    stats["stats"]["geoEnabled"] = {}
    stats["stats"]["quoted"] = {}
    
    stats["isFavList"] = []
    stats["geoEnabledList"] = []
    stats["quoteList"] = []
    stats["symbolList"] = []
    stats["hashtagList"] = []
    stats["urlList"] = []
    stats["possiblySensitiveList"] = []
    stats["retweetList"] = []
    
    #Divide the day into quarters
    stats["createDateList"] = []
    stats["locationList"] = []
    
    


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=False, help="JSON file containing user's tweets")
    args = vars(ap.parse_args())

    file = args['file']
    
    if(file is not None):
        with open(file) as data_file:    
            twitterAcount = json.load(data_file)
            
            
    
