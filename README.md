# tweetreader

CS 1026 Project. Read assignment pdf for instructions and rubric. happy_histogram.py made by Prof. Bauer.

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
