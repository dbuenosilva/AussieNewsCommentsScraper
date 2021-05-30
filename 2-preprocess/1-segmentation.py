# -*- coding: utf-8 -*-

##########################################################################
# Project: COMP6004 - A basic text miner
# File: 1-segmentation.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Sentence segmentation breaks a text into  
#              separate sentences.
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
import numpy as np
import nltk

path = str(pathlib.Path(__file__).resolve().parent) + "/"
sys.path.append(path)

segmentedTextDf = pd.DataFrame(data=None, index=None)

print("\nReading the raw data")

postsDf = pd.read_csv(path + '../1-gather/posts.csv',index_col=False)
commentsDf = pd.read_csv(path + '../1-gather/comments.csv',index_col=False)

# downloading the Punkt sentence segmenter and Gutenberg functions
nltk.download('punkt')
sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

for index, row in postsDf.iterrows():
    
    # encoding all text to UTF8
    #row["post_text"] = row["post_text"].encode("utf8")
    
    # converting all the text to lowercase
    row["post_text"] = row["post_text"].lower()
    
    # segmenting the text into senteces
    text = row["post_text"]
    
    # a list with all sentences
    myList = nltk.sent_tokenize(text)
    
    # converting the list to DataFrame to remove duplicates rows.
    sentencesList = pd.DataFrame( myList ,columns=['sentence'])     
    
    # removing duplicates sentence due to heading on news 
    print("\nChecking duplicated values:") 
    dups = sentencesList.duplicated()
    
    if not dups.any(): # Indicates if there is duplicate data with - True or false    
        print('\nThere is no duplicate information in the sentence list!')
    else:   
        print('\nDropping duplicated rowns')
        sentencesList.drop_duplicates(inplace=True)
        
    # saving dataframe
#    segmentedTextDf = segmentedTextDf.append( [ [ row["post_id"], sentencesList.to_dict(orient="list") ]], ignore_index=True  )
    segmentedTextDf = segmentedTextDf.append( [ [ row["post_id"], sentencesList.values ]], ignore_index=True  )
    
segmentedTextDf = segmentedTextDf.rename(columns={ segmentedTextDf.columns[0]: "post_id" })
segmentedTextDf = segmentedTextDf.rename(columns={ segmentedTextDf.columns[1]: "sentences" })
        
print("\nWriting a CSV file with all posts with segmented text")
segmentedTextDf.to_csv(path + "postsWithSegmentedText.csv",index=False)
