from flask import Flask
from feedgen.feed import FeedGenerator
import requests


app = Flask(__name__)

# The 25 most recent posts to a particular community 
@app.route('/<string:Community>')
def posts_by_specific_community(Community):
    print("community: ", Community)
    URL = r"http://localhost:5000/posts/" + f'{Community}'
    result = requests.get(URL)
    jsonResponse = result.json()
    fg = FeedGenerator()
    fg.id('http://localhost:5000/posts/Community')
    fg.title('All posts')
    fg.link( href='http://localhost:5000/posts/all',rel='alternate')
    fg.description('Printing all post')
    fg.language('en')
    # i = 0
    for each in jsonResponse:
    # print(each["PostID"], ":", each["Username"], ":" ,each["PostTitle"], ":",each["PostDate"], ":",each["Content"], ":",each["Community"], ":",each["URLResource"] )
        # if (i == 25):
        #     break
        fe = fg.add_entry()
        fe.title(each["PostTitle"])
        fe.author({'name':each["Username"]} )
        fe.link( href=each["URLResource"], rel='alternate' )
        fe.description(each["Content"])
        # i+=1
    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    return rssfeed  

# The 25 most recent posts to any community 
@app.route('/recent')
def posts_by_community():
    URL = "http://localhost:5000/posts"
    result = requests.get(URL)
    jsonResponse = result.json()
    fg = FeedGenerator()
    fg.id('http://localhost:5000/posts/')
    fg.title('All posts')
    fg.link( href='http://localhost:5000/posts/all',rel='alternate')
    fg.description('Printing any community')
    fg.language('en')
    i = 0
    for each in jsonResponse:
    # print(each["PostID"], ":", each["Username"], ":" ,each["PostTitle"], ":",each["PostDate"], ":",each["Content"], ":",each["Community"], ":",each["URLResource"] )
        if (i == 25):
            break
        fe = fg.add_entry()
        fe.title(each["PostTitle"])
        fe.author({'name':each["Username"]} )
        fe.link( href=each["URLResource"], rel='alternate' )
        fe.description(each["Content"])
        i+=1
    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    return rssfeed  

# The top 25 posts to a particular community, sorted by score
@app.route('/score/<string:Community>')
def score_by_community(Community):
    print("community: ", Community)
    URL = r"http://localhost:5000/posts/" + f'{Community}'
    vote = "http://localhost:5100/api/v1/resources/votes/all"
    resultURL = requests.get(URL)
    resultVote = requests.get(vote)
    jsonResponse = resultURL.json()
    jsonVoteResponse = resultVote.json()
    sort_obj = sorted(jsonVoteResponse,key=lambda x : x ['upVoted'], reverse=True)
    # print("Entire JSON response")
    fg = FeedGenerator()
    fg.id('http://localhost:5000/score/Community')
    fg.title('Score by Specific Community')
    fg.link( href='http://localhost:5100/api/v1/resources/votes/all',rel='alternate')
    fg.description('Printing specific community by score')
    fg.language('en')
    for data in sort_obj:
        for each in jsonResponse:
            if (data['communityID'] == each['Community']):
                print ("id: ", data['id'], " PostID: ", data['postID'], " upVote: ",data['upVoted'], " Community: ", each['PostID'],"\n")
                fe = fg.add_entry()
                fe.title(each["PostTitle"])
                fe.author({'name':each["Username"]} )
                fe.link( href=each["URLResource"], rel='alternate' )
                fe.content(each["Community"])
                break
    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    return rssfeed

# Top 25 posts to any community, sorted by score
@app.route('/score')
def posts_by_score_community():
    # print("community: ", Community)
    vote = "http://localhost:5100/api/v1/resources/votes/all"
    post = "http://localhost:5000/posts/all"
    queryVote = requests.get(vote)
    queryPost = requests.get(post)
    jsonResponseVote = queryVote.json()
    jsonResponsePost = queryPost.json()
    sort_obj = sorted(jsonResponseVote,key=lambda x : x ['upVoted'], reverse=True)
    fg = FeedGenerator()
    fg.id('http://localhost:5000//posts/score')
    fg.title('All communities')
    fg.link( href='http://localhost:5100/api/v1/resources/votes/all',rel='alternate')
    fg.description('Printing any community by score')
    fg.language('en')
    for each in sort_obj:
        # print ("Id: ", each["id"], " postID: ", each["postID"], " upVoted: " ,each["upVoted"], " downVoted: ",each["downVoted"],"communityID: ",each["communityID"],"\n")
        for post in jsonResponsePost:
            if each['postID'] == post['PostID']:
                print("Community: ", post["Community"], "\n" )
                # print ("Id: ", each["id"], " postID: ", each["postID"], " upVoted: " ,each["upVoted"], " downVoted: ",each["downVoted"],"communityID: ",each["communityID"],"\n")
                fe = fg.add_entry()
                fe.title(post["PostTitle"])
                fe.author({'name':post["Username"]} )
                fe.link( href=post["URLResource"], rel='alternate' )
                fe.content(post["Community"])
                # break
    rssfeed  = fg.rss_str(pretty=True) # Get the RSS feed as string
    return rssfeed  

    
# posts_by_score_community()
