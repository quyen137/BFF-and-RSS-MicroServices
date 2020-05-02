# cpsc449 Project 2 BFF and Rss

## Steps to run: 
```sh
Install Flask
$ pip3 install --user Flask-API python-dotenv
```
```sh
Install Request
$ pip3 install --user requests
```
```sh
Install Gunicorn3 & foreman 
$ sudo apt install --yes gunicorn3
$ sudo apt install --yes ruby-foreman

```
```sh
Install FeedGenerator
$ sudo apt update
$ sudo apt install --yes python3-lxml
$ pip3 install --user feedgen

```
## Current issue </br>
```sh
For this project, each microservices will be given a default port to ensure that all microservices will work properly all
	•Posting microservices: localhost:5000/post/posts/all 	
	•Voting microservices: localhost:5100/api/v1/resources/votes/all 
	•BFF microservices: localhost:5200/recent

```
# Rss feeds provided by the BFFF Microservices </br>
### The 25 most recent posts to any community  </br>
```sh
http://localhost:5200/recent
```
### The 25 most recent posts to a particular community  </br>
```sh
http://localhost:5200/<string>/<int> 
http://localhost:5200/school/25 

```
### Top 25 posts to any community, sorted by score </br>
```sh
http://localhost:5200/score 
```
### The top 25 posts to a particular community, sorted by score</br>
```sh
http://localhost:5200/score/<string>
http://localhost:5200/score/school

```
### The hot 25 posts to any community, ranked using Reddit hot ranking algorithm</br>
```sh
http://localhost:5200/hot 
```