# -*- coding: utf-8 -*-
##########################################################################
# Project: COMP6004 - A basic text miner
# File: textMiner.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Miner collected texts from Australian News Facebook fan pages.
#
#
#
##########################################################################
# Maintenance                            
# Author: 
# Date: 
# Description:  
#
##########################################################################>

import sys
import pathlib
import pandas as pd
import collections
import matplotlib.pyplot as plt 

path = str(pathlib.Path(__file__).resolve().parent) + "/"
sys.path.append(path)
sys.path.append(path + "1-gather")
sys.path.append(path + "2-preprocess")
sys.path.append(path + "3-indexing")
sys.path.append(path + "4-mining")
sys.path.append(path + "5-analysis")

## Customised modules:
import newsScraper
import segmentation  as step01
import tokenization  as step02
import tagging       as step03
import lemmatization as step04
import stopWords     as step05
import dependencyParsing as step06
import clustering    as clustering 
import model         as classficator


"""
**************************************************************
                         GATHERING DATA 
**************************************************************

Fan pages to retrieve posts and comments:
    
#https://www.facebook.com/abcnews.au
https://www.facebook.com/sbsnews/
https://www.facebook.com/9News/
https://www.facebook.com/7NewsAustralia/
https://www.facebook.com/10NewsFirst/
https://www.facebook.com/news.com.au/

*** Facebook may block your IP due to scraper ***

"""

fanPages = [ "abcnews.au", "sbsnews", "9News", "7NewsAustralia",
             "10NewsFirst", "news.com.au" ]

answer = input("Do you want to download today's news and its comments on Facebook? (yes or no )\n") 
if answer == "yes": 
    print("\nRetrieving News and comments from Facebook Fan pages:\n")
    print(fanPages)
        
    print("\nThis process can take a long time. Please be patient...\n")
   
    allPostsDf, allCommentsDf = newsScraper.getPostAndComments(fanPages, offset = 10)

    print("\nWriting a CSV file with all posts...")
    allPostsDf.to_csv(path + "data/posts.csv",index=False)
    
    print("\nWriting a CSV file with all posts comments...")
    allCommentsDf.to_csv(path + "data/comments.csv",index=False)

elif answer == "no": 
    print("Reading the file " + path + "data/posts.csv")    
    postsDf = pd.read_csv(path + 'data/posts.csv',index_col=False)
    
    print("Reading the file " + path + "data/comments.csv")        
    commentsDf = pd.read_csv(path + 'data/comments.csv',index_col=False)
    
else: 
    print("Please enter yes or no")
    sys.exit()

"""
**************************************************************
                         PREPROCESSING TASKS 
**************************************************************
"""

print("\nSegmenting each post into sentences")
segmentedTextDf = step01.segmentation( postsDf , path)
    
print("\nTokenising each sentence into tokens")    
tokenizedTextList = step02.tokenization( segmentedTextDf, path )

print("\nTagging each token for all post sentences")    
taggedTextList = step03.tagging( tokenizedTextList, path )

print("\nLemmatization each token for all post sentences")    
lemmatizedTextList = step04.lemmatization( taggedTextList, path )

print("\nRemoving stopwords from all posts")    
cleannedTextList = step05.removingStopWords( lemmatizedTextList, path )

print("\nBuilding dependency parsing in sentences (grammar to be defined!)")    
ParsedTextList = step06.dependencyParsing( cleannedTextList, path )


"""
**************************************************************
                         ANALYSING RESULTS
**************************************************************

 Classifying the posts according trained model on the BBC news 
 dataset and labels retrieved from Kaggle """

print("\nClassifying the post according to BBC news dataset and labels from Kaggle ")
myModel, vectorizer = classficator.getModel()

data = []
for post in cleannedTextList:
        
    textList = []    
    textRaw  = ""
    
    for sentences in post[1]: # 1 are sentences; 0 is the post_id
        #print("\nCluster of post ",post[0])

        for word in sentences:
             textList.append(word)
             textRaw += " " + word 
    
    # Create list to export into a dataframe after this loop
    data.append( [ post[0], textRaw ] )             

""" Unsuccessfull clustering 
    print("Clustering the post")

    iterableText = iter(textList)            
    cluster = clustering.cluster_texts(textList) 

""" 

finalTextsDF = pd.DataFrame(data=data, index=None, columns=["post_id","text"])
   
finalTextvector = vectorizer.transform(finalTextsDF.text)

results = myModel.predict(finalTextvector)

## 0 - business, 1 -entertainment, 2 - politics, 3 - sport, 4 - tech
labels = ["business", "entertainment", "politics", "sport", "tech", "other"]

labels[results[0]]

"""
**************************************************************
                        PLOTTING INFORMATION
**************************************************************
"""
# Print most common word, idea retrieve from
# https://towardsdatascience.com/very-simple-python-script-for-extracting-most-common-words-from-a-story-1e3570d0b9d0

# Creating a dictionary like { word : count } 
wordcount = {}

for post in cleannedTextList:
    for sentences in post[1]: # 1 are sentences; 0 is the post_id
            for word in sentences:
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word]+= 1

    
# Converting the dictionary to DataFrame to plot the results.
wordcountDf = pd.DataFrame(wordcount.items(), columns=['word','Count'])
    
n_print = int(input("How many most common words to print: "))
print("\nOK. The {} most common words are as follows\n".format(n_print))
word_counter = collections.Counter(wordcount)
for word, count in word_counter.most_common(n_print):
    print(word, ": ", count)


""" Histogram of word frequency """

#x = wordcountDf['word']
#plt.hist(x, bins=10)
#plt.xlabel('Number of Words in Description')
#plt.ylabel('Frequency')
#plt.show()

""" Bar chart word most used """
DftoPlot = wordcountDf.sort_values("Count", axis=0,ascending=False)[:n_print]
ax = DftoPlot.plot.bar(x='word', y='Count', rot=90)

""" Text per category """

# Creating a dataframe with results
categorisedResults = []                        
for x in results:
    categorisedResults.append(labels[x])

DftoPlot = pd.DataFrame(data=categorisedResults, index=None, columns=["category"])

DftoPlot = DftoPlot["category"].value_counts().to_frame()

plot = DftoPlot.plot.pie(y='category', figsize=(5, 5))
