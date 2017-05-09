import csv
import os
import argparse
import re
import json

def toCSV(jsonWeights,fileName):
    x = jsonWeights
    regex = r"(weightResults_noise)(_\d\.\d+_\d+_\d+)?\/(weight)(.*)(\.)"
    match = re.search(regex,fileName)
    print fileName
    # print match.group(2)
    
    RESULTS_DIR = "csvResults_noise" + str(match.group(2))
    print RESULTS_DIR 
    
    if not os.path.exists(RESULTS_DIR):
        os.mkdir(RESULTS_DIR)
    
    print match.group(4)
    
    f = csv.writer(open(os.path.join(RESULTS_DIR, "csv" + match.group(4)) + ".csv", "wb+"))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["decision", "iteration", "geo_enabled_list", "hashtag_list", "is_fav_list","possibly_sensitive_list","protected","quote_list","retweet_list","symbol_list","time_quarter","timezone_list","url_list"])

    for weightsRow in x:
        f.writerow([weightsRow["decision"],
                    weightsRow["iteration"],
                    weightsRow["weights"]["geo_enabled_list"],
                    weightsRow["weights"]["hashtag_list"],
                    weightsRow["weights"]["is_fav_list"],
                    weightsRow["weights"]["possibly_sensitive_list"],
                    weightsRow["weights"]["protected"],
                    weightsRow["weights"]["quote_list"],
                    weightsRow["weights"]["retweet_list"],
                    weightsRow["weights"]["symbol_list"],
                    weightsRow["weights"]["time_quarter"],
                    weightsRow["weights"]["timezone_list"],
                    weightsRow["weights"]["url_list"]])

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
                    jsonWeights = json.load(data_file)
                    toCSV(jsonWeights, os.path.join(dir,file))
            except Exception as e:
                print(str(e))
                print("Problem file:" + os.path.join(dir,file))
            
    elif(file is not None):
        with open(file) as data_file:    
            jsonWeights = json.load(data_file)
            toCSV(jsonWeights, file)

#regex = r"(weightResults_0.5_10_100\/)(weight)(.*)(\.)"
#match = re.search(regex,fileName)
#print fileName
#print match.group(3)


    
