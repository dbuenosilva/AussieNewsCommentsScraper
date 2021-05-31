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

import sys
import pathlib
import pandas as pd

path = str(pathlib.Path(__file__).resolve().parent) + "/"
sys.path.append(path)

taggedTextDf = pd.DataFrame(data=None, index=None)

print("\nReading the data with tokens.")

postsDf = pd.read_csv(path + 'postsWithSegmentedText.csv',index_col=False)
#commentsDf = pd.read_csv(path + 'commentsWithSegmentedText.csv',index_col=False)

for index, row in postsDf.iterrows():
    
    # converting all the text to lowercase
    print("Tokenising sentenses of post ", row["post_id"])
    
    # converting to array ( each line is a sentence )
    listOfSentences = row["sentences"].splitlines()

    # removing special caracters salved in the CSV
    i = 0
    while i < len(listOfSentences):
        listOfSentences[i] = listOfSentences[i].replace("[","").strip().replace("'","")
        listOfSentences[i] = listOfSentences[i].replace("]","").strip().replace("'","")
        i+=1
    
    # 
    
    
    
    # 
    
        
        


        
        
        
        
        
        
        
        
        
        