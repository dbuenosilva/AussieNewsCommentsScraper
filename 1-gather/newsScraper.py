# -*- coding: utf-8 -*-

##########################################################################
# Project: COMP6004 - A basic text miner
# File: newsScraper.py
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Gathering the latest news and comments on the major 
#              Australian news fan pages and save them to a CSV file.
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

from facebook_scraper import get_posts


##########################################################################
# Function: getPostAndComments 
# Author: Diego Bueno - d.bueno.da.silva.10@student.scu.edu.au 
# Date: 30/05/2021
# Description: Get posts and comments from a list of fan pages.
# 
# Parameters: fanPages - a list of fan pages id
#             offset   - number of pages to retrieve
# 
# Return:     [ allPostsDf, 
#               allCommentsDf ] - dataframes with all post and
#                                 all comments.
#
##########################################################################

def getPostAndComments(fanPages, offset):

    allPostsDf    = pd.DataFrame()
    allCommentsDf = pd.DataFrame()
    
    for fanpageId in fanPages:
    
        results =  get_posts(fanpageId, pages=offset, options={"comments": True})
        for post in results:
            
            print("retrieving post id ",post["post_id"],"...") 
        
            # array with only relevant information about this post       
            data = [ [ post["post_id"],post["username"],post["time"],post["post_url"],
                    post["link"],post["post_text"],post["comments"],
                    post["shares"],post["likes"] ] ]    
        
            # salving this post in a temp dataframe
            postDf = pd.DataFrame(data, columns = 
                               [ "post_id", "username", "time", 
                                "post_url", "link", "post_text", 
                                "comments", "shares", "likes"])
        
            # adding to futher posts
            allPostsDf = allPostsDf.append(postDf)
        
            # getting all comments from this post
            thisPostcommentsDf = pd.DataFrame(post["comments_full"])
            
            # adding to futher comments
            allCommentsDf = allCommentsDf.append(thisPostcommentsDf)
            
    return( allPostsDf, allCommentsDf )



""" Fan pages to retrieve posts and comments:
    
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


allPostsDf, allCommentsDf = getPostAndComments(fanPages, offset = 10)

# Writing a CSV file with all posts
allPostsDf.to_csv(path + "posts.csv",index=False)

# Writing a CSV file with all posts comments
allCommentsDf.to_csv(path + "comments.csv",index=False)

