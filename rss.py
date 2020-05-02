from flask import Flask
from feedgen.feed import FeedGenerator
import requests
from datetime import datetime, timedelta
from math import log

app = Flask(__name__)

# The 25 most recent posts to a particular community 
@app.route('/<string:Community>/<int:n>')
def posts_by_specific_community(Community,n):
    URL = r"http://localhost:5000/posts/" + f'{Community}' + r"/" + f'{n}'
    result = requests.get(URL)
    jsonResponse = result.json()
    fg = FeedGenerator()
    fg.id('http://localhost:5200/<string:Community>')
    fg.title('The 25 most recent posts to a particular community ')
    fg.link( href='http://localhost:5200/<string:Community>',rel='alternate')
    fg.description('Printing all post')
    fg.language('en')
    i = 0
    for each in jsonResponse:
        if (i == 25):
            break
        fe = fg.add_entry()
        fe.id(str(each["PostID"]))
        fe.title(each["PostTitle"])
        fe.author({'name':each["Username"], 'email':'default@csu.fullerton.edu'} )
        fe.link( href=each["URLResource"], rel='alternate' )
        fe.description(each["Content"])
        i+=1
    rssfeed  = fg.rss_str(pretty=True) 
    return rssfeed  

# The 25 most recent posts to any community 
@app.route('/recent')
def posts_by_community():
    URL = "http://localhost:5000/posts?n=25"
    result = requests.get(URL)
    jsonResponse = result.json()
    fg = FeedGenerator()
    fg.id('http://localhost:5200/recent')
    fg.title('The 25 most recent posts to any community ')
    fg.link( href='http://localhost:5200/recent',rel='alternate')
    fg.description('Printing any community')
    fg.language('en')
    i = 0
    for each in jsonResponse:
        if (i == 25):
            break
        fe = fg.add_entry()
        fe.id(str(each["PostID"]))
        fe.title(each["PostTitle"])
        fe.author({'name':each["Username"], 'email':'default@csu.fullerton.edu'} )
        fe.link( href=each["URLResource"], rel='alternate' )
        fe.description(each["Content"])
        i+=1
    rssfeed  = fg.rss_str(pretty=True)
    return rssfeed  

# The top 25 posts to a particular community, sorted by score
@app.route('/score/<string:Community>')
def score_by_community(Community):
    post = r"http://localhost:5000/posts/" + f'{Community}' + r"/25"
    resultPost = requests.get(post)
    jsonResponse = resultPost.json()
    mylist = []
    for each in jsonResponse:
        vote = r"http://127.0.0.1:5100/vote/" + f'{each["PostID"]}'
        queryVote = requests.get(vote)
        jsonResponseVote = queryVote.json()
        score = jsonResponseVote['upvote'] - jsonResponseVote['downvote']
        mylist.append({'ID': each['PostID'], 'score':score})
    sort_obj = sorted(mylist,key=lambda x : x ['score'], reverse=True)
    fg = FeedGenerator()
    fg.id('http://localhost:5200/score/<string:Community>')
    fg.title('The top 25 posts to a particular community, sorted by score')
    fg.link( href='http://localhost:5200/score/<string:Community>',rel='alternate')
    fg.description('Printing specific community by score')
    fg.language('en')
    temp = 0
    for obj in sort_obj:
        for each in jsonResponse:
            if temp == 25:
                break
            if (each["PostID"] == obj["ID"]):
                fe = fg.add_entry()
                fe.id(str(each["PostID"]))
                fe.title(each["PostTitle"])
                fe.author({'name':each["Username"], 'email':'default@csu.fullerton.edu'} )
                fe.link( href=each["URLResource"], rel='alternate' )
                fe.content(each["Community"])
                temp+=1
                break
    rssfeed  = fg.rss_str(pretty=True)
    return rssfeed  

# Top 25 posts to any community, sorted by score
@app.route('/score')
def posts_by_score_community():
    vote = "http://localhost:5100/toppostscore/25"
    post = "http://localhost:5000/posts/all"
    queryVote = requests.get(vote)
    queryPost = requests.get(post)
    jsonResponseVote = queryVote.json()
    jsonResponsePost = queryPost.json()
    # sort_obj = sorted(jsonResponseVote,key=lambda x : x ['upVoted'], reverse=True)
    fg = FeedGenerator()
    fg.id('http://localhost:5200/score')
    fg.title('Top 25 posts to any community, sorted by score')
    fg.link( href='http://localhost:5200/score',rel='alternate')
    fg.description('Printing any community by score')
    fg.language('en')
    i = 0
    for each in jsonResponseVote:
        for post in jsonResponsePost:
            if each['postID'] == post['PostID']:
                if (i == 25):
                    break
                fe = fg.add_entry()
                fe.id(str(post["PostID"]))
                fe.title(post["PostTitle"])
                fe.author({'name':post["Username"], 'email':'default@csu.fullerton.edu'} )
                fe.link( href=post["URLResource"], rel='alternate' )
                # fe.content({'content':post["Content"], 'src':'http://localhost:5000/posts/all', 'type':post["CDATA"]} )
                fe.description(post["Community"])
                i+=1
                break
    rssfeed  = fg.rss_str(pretty=True)
    return rssfeed  

    
# The hot 25 posts to any community, ranked using Reddit's "hot ranking" algorithm
@app.route('/hot')
def hot_post():
    post = "http://localhost:5000/posts/all"
    queryPost = requests.get(post)
    jsonResponsePost = queryPost.json()
    mylist = []
    for each in jsonResponsePost:
        second = epoch_seconds(each['PostDate'])
        vote = r"http://127.0.0.1:5100/vote/" + f'{each["PostID"]}'
        queryVote = requests.get(vote)
        jsonResponseVote = queryVote.json()
        result = hotPost(jsonResponseVote['upvote'],jsonResponseVote['downvote'],second)
        mylist.append({'ID': each['PostID'], 'score':result})
    sort_obj = sorted(mylist,key=lambda x : x ['score'], reverse=True)
    print(mylist,"\n")
    print(sort_obj, "\n")
    fg = FeedGenerator()
    fg.id('http://localhost:5200/hot')
    fg.title('The hot 25 posts to any community, ranked using Reddit hot ranking algorithm')
    fg.link( href='http://localhost:5200/hot',rel='alternate')
    fg.description('Printing out 25 Hot Trending Posts')
    fg.language('en')
    temp = 0
    for obj in sort_obj:
        for post in jsonResponsePost:
            if temp == 25:
                break
            if (post["PostID"] == obj["ID"]):
                fe = fg.add_entry()
                fe.id(str(post["PostID"]))
                fe.title(post["PostTitle"])
                fe.author({'name':post["Username"], 'email':'default@csu.fullerton.edu'} )
                fe.link( href=post["URLResource"], rel='alternate' )
                fe.description(post["Community"])
                temp +=1
                break
    rssfeed  = fg.rss_str(pretty=True)
    return rssfeed  


def epoch_seconds(PostDate):
    temp = PostDate.split('.')[0]
    format = "%Y-%m-%d %H:%M:%S"
    date = datetime.strptime(temp,format)   
    value = date.timestamp()
    return (value)

def hotPost(upVoted, downVoted, date):
    score = int(upVoted) - int(downVoted)
    order = log(max(abs(score), 1), 10)
    sign = 1 if score > 0 else -1 if score < 0 else 0
    seconds =  date - 1134028003.0
    return (round(sign * order + seconds / 45000, 7))
