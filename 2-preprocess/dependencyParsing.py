# -*- coding: utf-8 -*-

##########################################################################
# Project: COMP6004 - A basic text miner
# File: 6-dependencyParsing.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Identify how words relate to each other amoung sentencens.
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

def dependencyParsing(cleannedStopWordsTextList, path):

  
  # Dataframe to save result and export to CSV file
  parsedTextDf = pd.DataFrame(data=None, index=None)
  parsedTextList = []

  # a simple example of grammar ( TO BE DEFINED  )
  # https://www.nltk.org/book/ch08.html
  # http://www.nltk.org/howto/grammar.html
  my_grammar = nltk.CFG.fromstring("""
    S -> NP VP
    PP -> P NP
    NP -> Det N | Det N PP | 'I'
    VP -> V NP | VP PP
    Det -> 'an' | 'my'
    N -> 'australia' | 'country'
    N -> 'scomo' | 'morrison'    
    N -> 'nlfa' | 'football'      
    V -> 'play'
    P -> 'in' | 'on'
   """)

  print(my_grammar)
  

  cleannedStopWordsTextList = [ ["examplePost", [ [ "scomo", "play", "nlfa", "in", "australia"]]] ]
      
  for post in cleannedStopWordsTextList:

        print("\nParsing dependency in the post id ", post[POST_ID])                       
        
        for sentences in post[SENTENCES]:
                      
              #parser = nltk.ChartParser(my_grammar)
              rd_parser = nltk.RecursiveDescentParser(my_grammar)
              print(sentences)
              generated = rd_parser.parse(sentences)
              for tree in generated:
                  print(tree)
                              
  # return list with all parsed text posts  
  return(generated)                 
        
        
        
        