from flask import Flask
from feedgen.feed import FeedGenerator
import requests

import datetime 
from rfeed import *

app = Flask(__name__)

# @app.route("/")
# def home():
#     return '''<h1>Testing</h1>'''


@app.route("/service/")
def posts_by_community():
    result = requests.get('http://localhost:5000/posts/all')
    result.raise_for_status()
    
    jsonResponse = requests.get('http://localhost:5000/posts/all').json()
    print("Entire JSON response")
    # print(jsonResponse)
    # fg = FeedGenerator()
    # for each in jsonResponse:
    #     # print(each["PostID"], ":", each["Username"], ":" ,each["PostTitle"], ":",each["PostDate"], ":",each["Content"], ":",each["Community"], ":",each["URLResource"] )
    #     fg = FeedGenerator()
    #     fg.id(each["PostID"])
    #     fg.title(each["PostTitle"])
    #     fg.author({'name':each["Username"]} )
    #     fg.link( href=each["URLResource"], rel='alternate' )
    #     fg.description(each["Content"])
    #     fg.language('en')
    #     rssfeed = fg.rss_str(pretty=True)
        
    # print(rssfeed)

    for each in jsonResponse:
        # print(each["PostID"], ":", each["Username"], ":" ,each["PostTitle"], ":",each["PostDate"], ":",each["Content"], ":",each["Community"], ":",each["URLResource"] )
        item = Item(
            title = each["PostTitle"],
            link = "http://www.example.com/articles/1", 
            description = "This is the description of the first article",
            author = "Santiago L. Valdarrama",
            pubDate = datetime.datetime(2014, 12, 29, 10, 00))

        feed = Feed(
            title = "Sample RSS Feed",
            link = "http://www.example.com/rss",
            description = "This is an example of how to use rfeed to generate an RSS 2.0 feed",
            language = "en-US",
            lastBuildDate = datetime.datetime.now(),
            items = [item])
    return(feed.rss())
