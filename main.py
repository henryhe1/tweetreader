"""
This Python program reads tweets from a txt file and determines the timezone it was tweeted in.
Then, using another text file of keywords and sentiment values, creates a dictionary.
The program then assigns the sentiment values to the tweets which contain the keywords.
The happiness score per tweet is calculated by dividing the total sentiment value by the number of keywords found.
Then, a happiness level per timezone is computed by dividing the total happiness score of all tweets by the number of tweets.
Prints average happiness score per timezone and the total number of tweets per timezone.
Displays using happy_histogram.py GUI.

Author: Henry He
Student #: 250869172
Course: CS1026A, Assignment 3
Instructor: Jordan van Dyk
Language: Python 3.4
Date modified: November 18 2015

"""

import happy_histogram

#Timezone boundaries, given
LAT_MIN = 24.660845
LAT_MAX = 49.189787
LONG_EASTERN = -67.444574
LONG_CENTRAL = -87.518395
LONG_MOUNTAIN = -101.998892
LONG_PACIFIC = -115.236428
LONG_MIN = -125.242264

def readKeywords():

    keywordFile = input("Enter keywords filename: ")

    try:
        f = open(keywordFile + ".txt", "r")
    except IOError:
        print("Could not open file.")

    keywordDict = {} #initialize new dictionary

    for line in f:
        keywordList = line.split(",")
        hapValue = keywordList[1]
        hapValue = int(hapValue.strip()) # cast to int and strip \n

        keywordDict[keywordList[0]] = hapValue # new dictionary entry

    f.close()

    return keywordDict  # return the entire dictionary


def readTweets():

    tweetFile = input("Enter tweet filename: ")

    try:
        g = open(tweetFile + ".txt", "r")
    except IOError:
        print("Could not open file.")

    #initialize new lists
    eastern = []
    central = []
    mountain = []
    pacific = []

    for line in g:

        tweetList = line.split(" ", 5) # keep tweet as one string for now
        lat = tweetList[0]
        lat = float(lat.strip("[,"))
        long = tweetList[1]
        long = float(long.strip("]"))
        tweet = tweetList[5] # keep tweet as one string for now
        tweet = tweet.rstrip() # strip \n

        #sorting tweets into timezone lists

        if LAT_MIN < lat < LAT_MAX: #all timezones within lat range
            if LONG_EASTERN > long > LONG_CENTRAL:
                eastern.append(tweet)
            elif LONG_CENTRAL > long > LONG_MOUNTAIN:
                central.append(tweet)
            elif LONG_MOUNTAIN > long > LONG_PACIFIC:
                mountain.append(tweet)
            elif LONG_PACIFIC > long > LONG_MIN:
                pacific.append(tweet)

    g.close()

    return eastern, central, mountain, pacific #return all timezone lists


def calcHap(tweets, keywords):

    nKeywords = 0 # per tweet
    sent = 0 #sentiment value for each keyword per tweet
    score = 0 #per timezone

    for i in tweets:
        for j in keywords:
            if j.upper() in i.upper(): # eliminates upper/lowercase dsicrepancy
                nKeywords += 1
                sent += keywords[j]
                # print(i, j, keywords[j], nKeywords, sent)

        if nKeywords > 0: #eliminates div by zero error
            score = score + (sent/nKeywords)
            # print(score)
            nKeywords = 0 # reset per tweet
            sent = 0

    if len(tweets) > 0: #eliminates div by zero error
        score = score / len(tweets) # div by total number of tweets
        return score, len(tweets) # return the two outputs
    else:
        return -1 # no tweets in this timezone



def main():

    keywordDict = readKeywords()
    # # for key in sorted(keywordDict):
    # #     print(key, keywordDict[key])

    eastern, central, mountain, pacific = readTweets()


    print("\neastern")
    score1, numTweets = calcHap(eastern, keywordDict)
    print(round(score1,2), numTweets)
    # for n in eastern:
    #     print(n)

    print("\ncentral")
    score2, numTweets = calcHap(central, keywordDict)
    print(round(score2,2), numTweets)
    # for n in central:
    #     print(n)

    print("\nmountain")
    score3, numTweets = calcHap(mountain, keywordDict)
    print(round(score3,2), numTweets)
    # for n in mountain:
    #     print(n)

    print("\npacific")
    score4, numTweets = calcHap(pacific, keywordDict)
    print(round(score4,2), numTweets)
    # for n in pacific:
    #     print(n)


    happy_histogram.drawSimpleHistogram(score1, score2, score3, score4)
    #
    # open("tweets.txt","r",encoding="utf-8")
    #
    # also few clarifications:
    # ignore tweets with no keywords...do you mean do not include in total tweets?
    # ignore tweets from outside the time zones

main()