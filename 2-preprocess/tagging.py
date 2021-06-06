# -*- coding: utf-8 -*-

##########################################################################
# Project: COMP6004 - A basic text miner
# File: 3-tagging.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Tagging by looking at each token find its
#              part of speech a noun, a verb, an adjective and so on.
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

# constants
POST_ID   = 0
SENTENCES = 1

def tagging(tokenizedTextList, path):
    
    taggedTextList = []
    taggedTextDf   = pd.DataFrame(data=None, index=None)
    
    # obtaining the resource averaged_perceptron_tagger
    nltk.download('averaged_perceptron_tagger')
    
    for post in tokenizedTextList:

        print("Tagging tokens of post ", post[POST_ID])                       
        
        taggedPost = []
        
        for sentences in post[SENTENCES]:
            
             # tagging tokens of each sentence
             taggedSentence = nltk.pos_tag(sentences)
             
             # append to the post its sentences (now tagged)
             taggedPost.append( taggedSentence )

        # append the result final ( tagged tokens of all posts )
        taggedTextList.append( [ post[POST_ID], taggedPost ]  )                

        # saving dataframe with the post_id and segmented sentences.
        taggedTextDf = taggedTextDf.append( [ [ post[POST_ID], taggedPost ] ], ignore_index=True  )
        
    taggedTextDf = taggedTextDf.rename(columns={ taggedTextDf.columns[0]: "post_id" })
    taggedTextDf = taggedTextDf.rename(columns={ taggedTextDf.columns[1]: "sentences" })
            
    print("\nWriting a CSV file with all posts with segmented text")
    taggedTextDf.to_csv(path + "data/postsWithTaggedTokens.csv",index=False)
        
    return(taggedTextList)
            

        
            
            
    
    
            
            
            
            
            
            
            
            
            
            