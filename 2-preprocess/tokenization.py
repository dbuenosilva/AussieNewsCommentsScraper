# -*- coding: utf-8 -*-

##########################################################################
# Project: COMP6004 - A basic text miner
# File: 2-tokenization.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Tokenization breaks a sentence into separate componentes
#              such as words, punctuations, etc.
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

import pandas as pd
from nltk.tokenize import word_tokenize


def tokenization(postsDf, path):
            
    # Df to save the results in a CSV file
    tokenizedTextDf = pd.DataFrame(data=None, index=None)
    
    # List object to be returned
    tokenizedTextList = []
    
    print("\nReading the file with the sentences")
    
    postsDf = pd.read_csv(path + 'data/postsWithSegmentedText.csv',index_col=False)
    #commentsDf = pd.read_csv(path + 'commentsWithSegmentedText.csv',index_col=False)
    
    for index, row in postsDf.iterrows():
        
        print("Tokenising sentenses of post id", row["post_id"])
        
        # converting to array ( each line is a sentence )
        listOfSentences = row["sentences"].splitlines()
    
        # removing special caracters salved in the CSV
        i = 0
        while i < len(listOfSentences):
            listOfSentences[i] = listOfSentences[i].replace("[","").strip().replace("'","")
            listOfSentences[i] = listOfSentences[i].replace("]","").strip().replace("'","")
            i+=1
        
        # Splitting the sentence into tokens
        tokensPerSentence = []
        for sentence in listOfSentences:
            tokensPerSentence.append(word_tokenize(sentence))   
            
        # tokens that will be returned in the list for each post_id
        tokenizedTextList.append( [ row["post_id"], tokensPerSentence ] )
            
        # saving dataframe with the post_id and segmented sentences
        # Results will be saved for analysis purposes.
        tokenizedTextDf = tokenizedTextDf.append( [ [ row["post_id"], tokensPerSentence ]], ignore_index=True  )
    
    # setting names on columns
    tokenizedTextDf = tokenizedTextDf.rename(columns={ tokenizedTextDf.columns[0]: "post_id" })
    tokenizedTextDf = tokenizedTextDf.rename(columns={ tokenizedTextDf.columns[1]: "tokenization" })
            
    print("\nWriting a CSV file with all posts with tokenized text")
    tokenizedTextDf.to_csv(path + "data/postsWithTokenizedTextDfText.csv",index=False)

    # Return a list with all post and its tokenized sentences 
    return(tokenizedTextList)

