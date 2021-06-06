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

import pandas as pd
import nltk

def segmentation( postsDf , path):
    
    segmentedTextDf = pd.DataFrame(data=None, index=None)
    
    # downloading the Punkt sentence segmenter and Gutenberg functions
    nltk.download('punkt')
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
    
    for index, row in postsDf.iterrows():
        
        # encoding all text to UTF8
        #row["post_text"] = row["post_text"].encode("utf8")
            
        # segmenting the text into senteces
        text = row["post_text"]
        
        # removing \t \r and \n caracteres
        #text = text.strip("\n\t\r")  # problems with strip here
        text = text.replace("\n"," ")
        text = text.replace("\t"," ")
        text = text.replace("\r"," ")
        
        # a list with all sentences
        myList = nltk.sent_tokenize(text)
            
        # converting the list to DataFrame to remove duplicates rows.
        sentencesList = pd.DataFrame( myList ,columns=['sentence'])     
        
        # removing duplicates sentence due to heading on news 
        print("\nChecking duplicated values from post id ", row["post_id"]) 
        dups = sentencesList.duplicated()
        
        if not dups.any(): # Indicates if there is duplicate data with - True or false    
            print('\nThere is no duplicate information in the sentences of post ', row["post_id"] )
        else:   
            print('\nDropping duplicated rowns from post id ', row["post_id"])
            sentencesList.drop_duplicates(inplace=True)
            
        # saving dataframe with the post_id and segmented sentences.
        segmentedTextDf = segmentedTextDf.append( [ [ row["post_id"], sentencesList.values ]], ignore_index=True  )
        
    segmentedTextDf = segmentedTextDf.rename(columns={ segmentedTextDf.columns[0]: "post_id" })
    segmentedTextDf = segmentedTextDf.rename(columns={ segmentedTextDf.columns[1]: "sentences" })
            
    print("\nWriting a CSV file with all posts with segmented text")
    segmentedTextDf.to_csv(path + "data/postsWithSegmentedText.csv",index=False)
    
    return(segmentedTextDf)




