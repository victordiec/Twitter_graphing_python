#Python3
import os
import array
import argparse
import random
from statistics import mean
from statistics import stdev

from timezonefinder import TimezoneFinder
tf = TimezoneFinder()

import json
from pprint import pprint
import re
import numpy as np
import math


RESULTS_DIR = "noise"

def make_noise(fileName,twitterStats):
    
    name = re.search('([\w]+)\.',fileName)
    name = name.group(0)
    # print(name)
    
    bin_list_stat_dict = {
        "quote_list":"quoted",
        "is_fav_list":"fav",
        "retweet_list":"retweet",
        "geo_enabled_list":"geo_enabled",
        "hashtag_list":"hash",
        "symbol_list":"symbol",
        "url_list":"url",
        "possibly_sensitive_list":"url_possibly_sensitive",
        "protected":"protected",
    };
    
    freq_list_stat_dict = {
        "time_quarter":"time_quarter_frequency",
        "timezone_list":"timezone_freq"
    }
    
    for key in twitterStats:
        # print(key)
        
        #Binary Key
        if(key in bin_list_stat_dict):
            
            mn = twitterStats["stats"][bin_list_stat_dict[key]]["mean"]
            std_dev = math.sqrt(twitterStats["stats"][bin_list_stat_dict[key]]["variance"])
            
            try:
                mn = 0.5 if mn == 0 else mn
                std_dev = 0.5 if std_dev == 0 else std_dev
                whiteNoise = np.random.normal(mn, std_dev, len(twitterStats[key]))
            except Exception as e:
                raise e
            # print(mean)
            # print(stddev)
            # print(whiteNoise)
            
            injectPoint = random.randint(len(twitterStats[key])/5, len(twitterStats[key]))
            
            for i in range(0, len(twitterStats[key])):
                
                if(i >= injectPoint):
                    #Ensuring we always have 0 or 1
                    twitterStats[key][i] = int((twitterStats[key][i] + round(whiteNoise[i])) % 2)
            
        #Frequency Key
        # elif key in ("time_quarter"):
        elif (key in freq_list_stat_dict):
            print(key)
            freq_list = []
            for zone in twitterStats["stats"][freq_list_stat_dict[key]]:
                # print(zone)
                # print(twitterStats["stats"][freq_list_stat_dict[key]][zone])
                freq_list.append(twitterStats["stats"][freq_list_stat_dict[key]][zone])
                
            # print(freq_list)
            freq_mean = mean(freq_list)
            freq_std_dev = stdev(freq_list)
            print(freq_mean)
            print(freq_std_dev)
            
            whiteNoise = np.random.normal(freq_mean, freq_std_dev, len(twitterStats[key]))
            injectPoint = random.randint(len(twitterStats[key])/5, len(twitterStats[key]))

            # print(max(twitterStats["stats"][freq_list_stat_dict[key]]))
            # print(int(max(twitterStats["stats"][freq_list_stat_dict[key]])))
            
            for i in range(0, len(twitterStats[key])):
                if(i >= injectPoint):
                    twitterStats[key][i] = int((twitterStats[key][i] + round(whiteNoise[i]/max(whiteNoise)*int(max(twitterStats["stats"][freq_list_stat_dict[key]]))))% int(max(twitterStats["stats"][freq_list_stat_dict[key]]))+1)
        
    
    with open(os.path.join(RESULTS_DIR, "noise" + name) + "json", 'w') as f:
        f.write(json.dumps(twitterStats, sort_keys=True,indent=1))
        

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
                    twitterStats = json.load(data_file)
                    make_noise(file,twitterStats)
            except Exception as e:
                print(str(e))
                print("Problem file:" + os.path.join(dir,file))
            
    elif(file is not None):
        with open(file) as data_file:    
            twitterStats = json.load(data_file)
            make_noise(file, twitterStats)