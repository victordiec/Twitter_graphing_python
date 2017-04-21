from random import randint
from random import randrange
from random import uniform
import math
import numpy
import json
import os
import argparse
import re

RESULTS_DIR = "weightResults"

#importing the JSON object to be analyzed

# You're going to have to refactor this later on...
# with open('statsBillNye.json') as data_file:
#     data = json.load(data_file)

#class for defining each tree object
class Tree(object):
    #method for initializing the new tree objects
    def __init__(self):
        self.featureSet = []
        self.weightedTotal = 0.0
    #method for setting a new value for the Tree's weighted total    
    def setWeightedTotal(self, newTotal):
        self.weightedTotal = newTotal
    #method for getting the value for the Tree's weighted total    
    def getWeightedTotal(self):
        return self.weightedTotal
    #method for changing the feature set of the tree object
    def setFeatures(self, newFeatureSet):
        self.featureSet = newFeatureSet
    #method for changing the feature set of the tree object
    def getFeatures(self):
        return self.featureSet


#This is the class for the actual algorithm
class RandomForest(object):
    
    data = {}
    
    def __init__(self, twitterData, numTrees):
        self.trees = []
        self.data=twitterData
        for x in range(numTrees):
            x = Tree()
            self.trees.append(x)
            
    #this method generates and assigns the randomized feature sets to the tree objects
    def generateFeatureSets(self, trees):
        baseFeatureSet = ['retweet_list','time_quarter','is_fav_list','protected','timezone_list','quote_list','geo_enabled_list','url_list','symbol_list','possibly_sensitive_list','hashtag_list']
        totalFeatures = len(baseFeatureSet)
        for tree in trees:
            tempFeatureSet = []
            tempFeatureSet.extend(baseFeatureSet)
            treeFeatureSet = []
            numFeatures = randint(2,5)
            while (numFeatures>0):
                if (len(tempFeatureSet) > 0):
                    newFeatureIndex = randint(0, len(tempFeatureSet)-1)
                else:
                    newFeatureIndex = 0
                treeFeatureSet.append(tempFeatureSet.pop(newFeatureIndex))
                numFeatures -= 1
            tree.setFeatures(treeFeatureSet)
    
    def newWeights(self, weights):
        new ={}
        new.update(weights)
        keys = ['retweet_list','time_quarter','is_fav_list','protected','timezone_list','quote_list','geo_enabled_list','url_list','symbol_list','possibly_sensitive_list','hashtag_list']
        maximumIndex = len(keys)-1
        index1 = randint(0,maximumIndex)
        index2 = randint(0,maximumIndex)
        change = 0.0
        while(index1 == index2):
            index2 = randint(0,maximumIndex)
        if(new[keys[index1]] > new[keys[index2]]):
            change = uniform(0.01,new[keys[index2]])
        elif(new[keys[index1]] < new[keys[index2]]):    
            change = uniform(0.01,new[keys[index1]])
        else:
            change = uniform(0.01,new[keys[index2]])
        if(randint(0,1) == 1):
            new[keys[index2]] = new[keys[index2]] + change
            new[keys[index1]] = new[keys[index1]] - change
        else:
            new[keys[index2]] = new[keys[index2]] - change
            new[keys[index1]] = new[keys[index1]] + change
        return new 
        
    def getTreeDecision(self, tree, currentWeights):
        tree.setWeightedTotal(0)
        workingSet = tree.getFeatures()
        #passing through each feature in the tree object's feature set
        for feat in workingSet:
            #pulling feature information from the JSON object
            if (feat == 'retweet_list'):
                valueSet = self.data['retweet_list']
                mean = self.data['stats']['retweet']['mean']
                variance = self.data['stats']['retweet']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            elif (feat == 'is_fav_list'):
                valueSet = self.data['is_fav_list']
                mean = self.data['stats']['fav']['mean']
                variance = self.data['stats']['fav']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            elif (feat == 'protected'):
                valueSet = self.data['protected']
                mean = self.data['stats']['protected']['mean']
                variance = self.data['stats']['protected']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            elif (feat == 'time_quarter'):
                frequencies = self.data['stats']['time_quarter_frequency']
                actualMean = 0
                for x in frequencies:
                    actualMean += frequencies[x]
                actualMean = actualMean / len(self.data[feat])
                actualVariance = 0
                for y in frequencies:    
                    actualVariance += (frequencies[y] - actualMean)**2
                actualVariance = actualVariance/len(self.data[feat])
                weight = currentWeights[feat]
            elif (feat == 'timezone_list'):
                frequencies = self.data['stats']['timezone_freq']
                actualMean = 0
                for x in frequencies:
                    actualMean += frequencies[x]
                actualMean = actualMean / len(self.data[feat])
                actualVariance = 0
                for y in frequencies:    
                    actualVariance += (frequencies[y] - actualMean)**2
                actualVariance = actualVariance/len(self.data[feat])
                weight = currentWeights[feat]
            elif (feat == 'quote_list'):
                valueSet = self.data['quote_list']
                mean = self.data['stats']['quoted']['mean']
                variance = self.data['stats']['quoted']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            elif (feat == 'geo_enabled_list'):
                valueSet = self.data['geo_enabled_list']
                mean = self.data['stats']['geo_enabled']['mean']
                variance = self.data['stats']['geo_enabled']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            elif (feat == 'url_list'):
                valueSet = self.data['url_list']
                mean = self.data['stats']['url']['mean']
                variance = self.data['stats']['url']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            elif (feat == 'symbol_list'):
                valueSet = self.data['symbol_list']
                mean = self.data['stats']['symbol']['mean']
                variance = self.data['stats']['symbol']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            elif (feat == 'possibly_sensitive_list'):
                valueSet = self.data['possibly_sensitive_list']
                mean = self.data['stats']['url_possibly_sensitive']['mean']
                variance = self.data['stats']['url_possibly_sensitive']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            elif (feat == 'hashtag_list'):
                valueSet = self.data['hashtag_list']
                mean = self.data['stats']['hash']['mean']
                variance = self.data['stats']['hash']['variance']
                std_Dev = math.sqrt(variance)
                weight = currentWeights[feat]
            
            #Solving each decision
            if (feat == 'time_quarter'):
                threshold = 0.5
                windowSize = 100
                means = []
                variances = []
                numShifts = len(self.data[feat]) - 99
                #incrementing window shifts
                for x in range(numShifts):##################
                    freqs = {}
                    #passing through each time quarter
                    
                    values = {}
                    
                    for i in range(4):
                        values[i] = []
                        freqs[i] = 0
                    
                    # for y in range(4):
                    #     values = []
                    #     #passing through the values in each time quarter
                    #     for z in range(windowSize):
                    #         value = self.data[feat][str(y)][x+z]
                    #         values.append(value)
                    #     #finding the frequency of each time quarter
                    #     freqs.append(sum(values)/windowSize)
                    
                    for z in range(windowSize):
                        value = self.data[feat][x+z]
                        values[value].append(1)
                    
                    for i in range(4):
                        freqs[i] = float(sum(values[i])/float(windowSize))
                        
                    #calculating the mean of this window
                    winMean = 0
                    for v in freqs:
                        winMean += freqs[v]*(v+1)
                    winMean = winMean/windowSize
                    means.append(winMean)
                    #using the window mean, calculating the window variance
                    var = 0
                    for f in freqs:    
                        var += (freqs[f] - winMean)**2
                    var = var/windowSize
                    variances.append(var)
                consistency = 0.0
                for m in means:
                    if(actualMean- math.sqrt(actualVariance) < m < actualMean + math.sqrt(actualVariance)):
                        consistency += 1
                #print "Consistency: ", consistency, ", Threshold: ", threshold
                consistency = consistency / len(means)
                if (consistency > threshold):
                    tree.setWeightedTotal(tree.getWeightedTotal() + 1*weight)
            elif (feat == 'timezone_list'):
                threshold = 0.5
                windowSize = 100
                means = []
                variances = []
                numShifts = len(self.data[feat]) - 99
                
                #incrementing window shifts
                for x in range(numShifts):##################
                    freqs = {}
                    values = {}
                    #passing through each timezone
                    
                    # for y in range(418):
                    #     values = []
                    #     #passing through the values in each timezone
                    #     for z in range(windowSize):
                    #         value = self.data[feat][str(y)][x+z]
                    #         values.append(value)
                    #     #finding the frequency of each timezone
                    #     freqs.append(sum(values)/windowSize)    
                    # #calculating the mean of this window
                    
                    for i in range(418):
                        values[i] = []
                        freqs[i] = 0
                        
                    for z in range(windowSize):
                        value = self.data[feat][x+z]
                        values[value].append(1)
                    
                    for i in range(418):
                        freqs[i] = float(sum(values[i])/float(windowSize))
                    
                    winMean = 0
                    for v in freqs:
                        winMean += freqs[v]*(v+1)
                    winMean = winMean/windowSize
                    means.append(winMean)       
                    #using the window mean, calculating the window variance
                    var = 0
                    for f in freqs:    
                        var += (freqs[f] - winMean)**2
                    var = var/windowSize
                    variances.append(var)
                    
                consistency = 0.0
                for m in means:
                    if(actualMean- math.sqrt(actualVariance) < m < actualMean + math.sqrt(actualVariance)):
                        consistency += 1
                #print "Consistency: ", consistency, ", Threshold: ", threshold
                consistency = consistency / len(means)
                if (consistency > threshold):
                    tree.setWeightedTotal(tree.getWeightedTotal() + 1*weight)
            else:
                #threshold = 0.5
                #for x in valueSet:
                #    if(mean-std_Dev < x < mean+std_Dev):
                #        tree.setWeightedTotal(tree.getWeightedTotal()+weight*1)
                threshold = 0.5
                windowSize = 100
                means = []
                variances = []
                numShifts = len(valueSet) - 99
                #incrementing window shifts
                for x in range(numShifts):##################
                    values = []
                    #passing through the values
                    for z in range(windowSize):
                        value = valueSet[x+z]
                        values.append(value)
                    #calculating the mean of this window
                    winMean = 0.0
                    for v in values:
                        winMean += values[v]
                    winMean = winMean/windowSize
                    
                    means.append(winMean)
                    #using the window mean, calculating the window variance
                    var = 0
                    for y in values:    
                        var += (values[y] - winMean)**2
                    var = var/windowSize
                    variances.append(var)
                
                consistency = 0.0
                #print "Mean:",mean, ",Std_dev:", std_Dev, "Means length", len(means)
                # #print means
                # sys.exit()
                
                for m in means:
                    if(mean- std_Dev < m < mean + std_Dev):
                        consistency += 1
                consistency = consistency / len(means)
                #print "Consistency: ", consistency, ", Threshold: ", threshold 
                if (consistency > threshold):
                    tree.setWeightedTotal(tree.getWeightedTotal() + 1*weight)
        return tree.getWeightedTotal()


def randomForestAlgorithm(twitterAccount, fileName):
    
    prevForestDec = 0 #initialize a value for the value of the previous decision; 0 at start as no decision has been made yet
    forest = RandomForest(twitterAccount, 100) #variable to hold the random forest object
    forest.generateFeatureSets(forest.trees) #calling the method to generate a feature set for each tree in the forest
    #the below dictionary initializes the weights for each feature (these are always 1)
    defaultWeights = {'retweet_list':1.0,'time_quarter':1.0,'is_fav_list':1.0,'protected':1.0,'timezone_list':1.0,'quote_list':1.0,'geo_enabled_list':1.0,'url_list':1.0,'symbol_list':1.0,'possibly_sensitive_list':1.0,'hashtag_list':1.0}
    
    # treeDecisions = [] #this list hold all the decisions of the forest for a particular set of weights
    
    #this list holds the average decision of each forest for each weight set
    overallDecisions = [] 
    
    weightSets =[] #list of the weight sets used in each iteration
    previousWeights = {} #dictionary for the values of weigths in the previous iteration
    currentWeights = defaultWeights #initialize dictionary for working set of weights in 
    
    # currForestDec = 0.0 #this is a variable to hold the decision of the forest for the current weights 
    prevForestDec = 0.0 #this is a variable to hold the decision of the forest for the previous weight set
    
    #Update dictionaries so that they all have the same key-value pairs as default weights
    previousWeights.update(defaultWeights)
    currentWeights.update(defaultWeights)
    
    stats = []
    
    
    #Number of times rnadom forest is called
    for iteration in range(10):
        
        #For each random forest, initialize the concluding decision of the forrest and the decision of each of its trees
        currForestDec = 0.0
        treeDecisions = []
        i = 0
        #For each tree in the forest
        for tree in forest.trees:
            i = i+1
            #Get the decision from this tree
            decision = float(forest.getTreeDecision(tree, currentWeights))
            # #print i, " Decision from tree:", decision
            
            # tree.setWeightedTotal(decision)
            sumOfWeights = 0.0
            
            #For each node in the decision tree, we find out the weight of that node to get the total weight of that tree
            #I.e. if Tree i uses f1, f2, f5 (0.1, 0.3, 0.2), we find out their relative weights in this "decision"
            for key in tree.getFeatures():
                sumOfWeights += currentWeights[key]
                #print "sum Weight:", sumOfWeights
            
            #Normalize the decision value to a percentage   
            decision = float(decision/sumOfWeights)*100
            #print i, decision
            # tree.setWeightedTotal(decision)
            
            #Add the decision to the list of decision and move to the next iteration
            treeDecisions.append(decision)
        
        #print "Tree Decisions:", treeDecisions
            
        
        currForestDec = sum(treeDecisions) #/len(treeDecisions)
        # stats[iteration-1]["decision"] = currForestDec
        stats.append({"weights":currentWeights, "decision":currForestDec, "iteration":iteration})
        #print 'Decision: %s' % currForestDec
        
        #Add this forest decision to the list of forests
        overallDecisions.append(currForestDec)
        #print 'Current Weights\n' , currentWeights
        
        
        ####This works/
        #base case for changing weights
        if(prevForestDec == 0):
            
            #Save the current decision as it is good
            prevForestDec = currForestDec
            
            #Reset current weights
            currentWeights = {}
            currentWeights.update(forest.newWeights(defaultWeights))
            #print "Updated current weights:", currentWeights
            
        #if new weights did better than old
        elif(prevForestDec < currForestDec):
            previousWeights = {}
            previousWeights.update(currentWeights)
            
            #print "updated previous weights:" , previousWeights
            
            #This did better
            prevForestDec = currForestDec
            currentWeights = {}
            currentWeights.update(forest.newWeights(previousWeights))
            #print "current weights:", currentWeights   
            
        #if new weights did worse or equal than previous
        else:
            currentWeights = {}
            currentWeights.update(forest.newWeights(previousWeights))
            #print "previous weights:", previousWeights
            #print "Updated current weights:", currentWeights
            
        ####This Works/
            
    regex = r"(statsResults\/)(stats)(.*)(\.)"
    match = re.search(regex,fileName)
    print fileName
    print match.group(3)
    with open(os.path.join(RESULTS_DIR, "weight" + match.group(3)) + ".json", 'w') as f:
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
                    randomForestAlgorithm(twitterAccount, os.path.join(dir,file))
            except Exception as e:
                print(str(e))
                print("Problem file:" + os.path.join(dir,file))
            
    elif(file is not None):
        with open(file) as data_file:    
            twitterAccount = json.load(data_file)
            randomForestAlgorithm(twitterAccount, file)