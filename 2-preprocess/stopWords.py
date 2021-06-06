# -*- coding: utf-8 -*-

##########################################################################
# Project: COMP6004 - A basic text miner
# File: 4-stopWords.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Removes stop words such as and, the, a, of, from etc.
#
#
##########################################################################
# Maintenance                            
# Author: 
# Date: 
# Description:  
#
##########################################################################>

import pandas as pd
import nltk
from nltk.corpus import stopwords

POST_ID   = 0
SENTENCES = 1

def removingStopWords(lemmatizedTextList, path):

  # Setting English stopwords.
  # set(stopwords.words('english'))
  
  # getting English stopwords.
  nltk.download('stopwords')
  stopWords = stopwords.words('english')
  
  # Dataframe to save result and export to CSV file
  cleannedStopWordsTextDf = pd.DataFrame(data=None, index=None)

  # Initialise the object NLTK Lemmatizer

  cleannedStopWordsTextList = []
      
  for post in lemmatizedTextList:

        print("\nChecking stopwords in the post id ", post[POST_ID])                       
        
        cleannedStopWordsPost = []
        
        for sentences in post[SENTENCES]:
            
             cleannedStopWordsSentence = []
          
             for word in sentences:        
                                  
                 if word in stopWords:
                     print("Removed stopword ", word)
                 elif word not in ["IN", "DT","CD","TO","PRP", "CC","MD","WRB","WP","WDT"]:                   
                     # Saving word to sentence list
                     cleannedStopWordsSentence.append(word)
                
             # append sentences to post list
             cleannedStopWordsPost.append( cleannedStopWordsSentence )

        # append lemmatized sentences to its posts result
        cleannedStopWordsTextList.append( [ post[POST_ID], cleannedStopWordsPost ]  )                

        # saving dataframe with the post_id and lemmatized text
        cleannedStopWordsTextDf = cleannedStopWordsTextDf.append( [ [ post[POST_ID], cleannedStopWordsPost ] ], ignore_index=True  )

        
  cleannedStopWordsTextDf = cleannedStopWordsTextDf.rename(columns={ cleannedStopWordsTextDf.columns[0]: "post_id" })
  cleannedStopWordsTextDf = cleannedStopWordsTextDf.rename(columns={ cleannedStopWordsTextDf.columns[1]: "text" })
            
  print("\nWriting a CSV file with all posts without stopwords")
  cleannedStopWordsTextDf.to_csv(path + "data/postsWithoutStopWords.csv",index=False)    
    
  # return list with all lemmatized text posts  
  return(cleannedStopWordsTextList)                 