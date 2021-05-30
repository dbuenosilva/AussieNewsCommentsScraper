# -*- coding: utf-8 -*-

from facebook_scraper import get_posts

posts =  get_posts('abcnews.au', pages=1, options={"comments": True})
i = 1;
for post in posts:
    print("post ",i)
    print(post['text'][:100])
    i=i+1;




"""
https://www.facebook.com/abcnews.au

https://www.facebook.com/sbsnews/

https://www.facebook.com/9News/

https://www.facebook.com/7NewsAustralia/

https://www.facebook.com/10NewsFirst/

https://blog.feedspot.com/australian_news_websites/

https://www.facebook.com/news.com.au/

"""
