# -*- coding: utf-8 -*-

##########################################################################
# Project: COMP6004 - A basic text miner
# File: 3-lemmatization.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Figuring out the lemma of each word in sentencens.
#
#
##########################################################################
# Maintenance                            
# Author: 
# Date: 
# Description:  
#
##########################################################################>

from nltk.corpus import wordnet
import pandas as pd
import nltk

POST_ID   = 0
SENTENCES = 1
WORD      = 0
POS       = 1

def lemmatization(taggedTextList, path):

  # donwloading wordnet resource
  nltk.download('wordnet')

  # Dataframe to save result and export to CSV file
  lemmatizedtDf = pd.DataFrame(data=None, index=None)

  # Initialise the object NLTK Lemmatizer
  lemmatizer         = nltk.stem.WordNetLemmatizer()    
  porterStem         = nltk.stem.PorterStemmer()
  
  lemmatizedTextList = []
  
  print("\nLemmatization with WordNet Stemmer.")
  applyPorter = input("Would you like also to apply Porter Stem for lemmatization? (yes or no )\n") 
    
  for post in taggedTextList:

        print("\n\nLemmatising tokens of post ", post[POST_ID])                       
        
        lemmatizedPost = []
        
        for sentences in post[SENTENCES]:
            
             lemmatizedSentence = []
             # Lemmatising tokens of each sentence
             for token in sentences:

                 # Converting to lower case
                 word = token[WORD].lower()

                 # Reducing the words with WordNet                   
                 nPos = get_wordnet_pos(token[1])                                  
                 if nPos:
                     lemmatizedToken = lemmatizer.lemmatize(word, nPos)
                 else:
                     lemmatizedToken = lemmatizer.lemmatize(token[POS])
                           
                 # Also reducing the words to the stem using Porter Stem
                 if applyPorter == "yes":  
                     lemmatizedToken = porterStem.stem(lemmatizedToken)

                 print("word: ", token[WORD])                 
                 print("Tagged POS: ", token[POS])                                  
                 print("Type of POS: ", get_wordnet_pos(token[POS]))                                 
                 print("lemmatizedToken: ", lemmatizedToken,"\n")
                  
                 # Removing Non-digits from the sentence
                 if lemmatizedToken.isalpha():
                     # Saving lemmatizedToken to sentence list
                     lemmatizedSentence.append(lemmatizedToken)
                
             # append lemmatized sentences 
             lemmatizedPost.append( lemmatizedSentence )

        # append lemmatized sentences to its posts result
        lemmatizedTextList.append( [ post[POST_ID], lemmatizedPost ]  )                

        # saving dataframe with the post_id and lemmatized text
        lemmatizedtDf = lemmatizedtDf.append( [ [ post[POST_ID], lemmatizedPost ] ], ignore_index=True  )

        
  lemmatizedtDf = lemmatizedtDf.rename(columns={ lemmatizedtDf.columns[0]: "post_id" })
  lemmatizedtDf = lemmatizedtDf.rename(columns={ lemmatizedtDf.columns[1]: "text" })
            
  print("\nWriting a CSV file with all posts with lemmatized text")
  lemmatizedtDf.to_csv(path + "data/postsWithlemmatizedTokens.csv",index=False)    
    
  # return list with all lemmatized text posts  
  return(lemmatizedTextList)




# Function retrieved from
# https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''