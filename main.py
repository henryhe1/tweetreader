"""
This Python program reads tweets from a txt file and determines the timezone it was tweeted in.
Then, using another text file of keywords and sentiment values, creates a dictionary.
The program then assigns the sentiment values to the tweets which contain the keywords.
Only full keywords were counted. Keywords which contained other keywords, such as 'greatest', were counted only once.
Punctuation was stripped from each word.
The happiness score per tweet is calculated by dividing the total sentiment value by the number of keywords found.
Then, a happiness level per timezone is computed by dividing the total happiness score of all tweets by the number of
tweets with keywords.
Tweets with no keywords and/or outside the timezone boundaries were ignored. Border cases included.
Prints average happiness score per timezone and the total number of tweets with keywords per timezone.
Displays using happy_histogram.py GUI.

Author: Henry He
Student #: 250869172
Course: CS1026A, Assignment 3
Instructor: Jordan van Dyk
Language: Python 3.4
Date modified: November 18 2015.

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
        print("Could not find file.") # exits if file doesn't exist

    keywordDict = {} #initialize new dictionary

    for line in f:
        keywordList = line.split(",") #split using , as delimiter
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
        print("Could not find file.") #exit if file cannot be found

    #initialize new lists for each timezone
    eastern = []
    central = []
    mountain = []
    pacific = []

    for line in g:

        tweetList = line.split(" ", 5) # split line into 6 sections
        lat = tweetList[0]
        lat = float(lat.strip("[,")) #strip bracket and cast to decimal
        long = tweetList[1]
        long = float(long.strip("]")) #strip bracket and cast to decimal
        tweet = tweetList[5] # keep tweet as one string, for now
        tweet = tweet.rstrip() # strip \n

        #sorting tweets into timezone lists

        if LAT_MIN <= lat <= LAT_MAX: #all timezones within lat range ... removed tweets outside range
            if LONG_EASTERN >= long > LONG_CENTRAL:
                eastern.append(tweet)
            elif LONG_CENTRAL >= long > LONG_MOUNTAIN:
                central.append(tweet)
            elif LONG_MOUNTAIN >= long > LONG_PACIFIC:
                mountain.append(tweet)
            elif LONG_PACIFIC >= long >= LONG_MIN:
                pacific.append(tweet)

    g.close()

    return eastern, central, mountain, pacific #return all timezone lists


def calcHap(tweets, keywords):

    nKeywords = 0 # per tweet
    sent = 0 #sentiment value for each keyword per tweet
    score = 0 #per timezone
    counter = 0

    for i in tweets:
        tweetList = i.split(" ") # split the tweet into individual words
        for j in tweetList: #iterate through the tweet words
            # print(j)
            j = j.strip('`1234567890~!#$%^&*()_+-={}|[]\\:”“";\':;?/>.<,') # didnt include @ because usernames don't indicate happiness at the moment of the tweet
            # print(j)
            for k in keywords: #iterate through the keywords
                if j.upper() == k.upper(): # eliminates upper/lowercase discrepancy, use == instead of "in" to avoid double counting keywords like 'greatest'
                    nKeywords += 1
                    sent += keywords[k] # sentiment value per tweet
                    #print(i, k, keywords[k], nKeywords, sent)

        if nKeywords > 0: #eliminates div by zero error
            score = score + (sent/nKeywords)
            #print(score)
            nKeywords = 0 # reset per tweet
            sent = 0
            counter += 1

    if counter > 0: #eliminates div by zero error
        score = score / counter # div by total number of tweets
        return score, counter # return the two outputs
    else:
        return -1 # no tweets in this timezone



def main():

    keywordDict = readKeywords()
    # # for key in sorted(keywordDict):
    # #     print(key, keywordDict[key])

    eastern, central, mountain, pacific = readTweets()


    print("\neastern")
    score1, numTweets = calcHap(eastern, keywordDict)
    print("%-15s %5.2f" % ("happiness", score1))
    print("%-15s %5.0d" % ("total tweets", numTweets))
    # for n in eastern:
    #     print(n)

    print("\ncentral")
    score2, numTweets = calcHap(central, keywordDict)
    print("%-15s %5.2f" % ("happiness", score2))
    print("%-15s %5.0d" % ("total tweets", numTweets))
    # for n in central:
    #     print(n)

    print("\nmountain")
    score3, numTweets = calcHap(mountain, keywordDict)
    print("%-15s %5.2f" % ("happiness", score3))
    print("%-15s %5.0d" % ("total tweets", numTweets))
    # for n in mountain:
    #     print(n)

    print("\npacific")
    score4, numTweets = calcHap(pacific, keywordDict)
    print("%-15s %5.2f" % ("happiness", score4))
    print("%-15s %5.0d" % ("total tweets", numTweets))
    # for n in pacific:
    #     print(n)


    happy_histogram.drawSimpleHistogram(score1, score2, score3, score4)


main()