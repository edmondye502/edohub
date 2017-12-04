from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import praw

def index(request):

	if not request.user.is_authenticated():
		return redirect('/accounts/login/')

	weather = temperature()
	reddit_posts = reddit('kpop')

	content = {'username': request.user.username, 'temp': weather, 'reddit': reddit_posts}

	return render(request, 'hub/home.html', content)


def temperature():
	zipcode = '94122'
	r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=d7608eb9909f2561fa7a7a1b62d078b5')
	temp_k = float(r.json()['main']['temp'])
	temp_f = int(round((temp_k - 273) * 1.8 + 32))
	return temp_f

def reddit(subreddit):
	reddit = praw.Reddit(client_id = 'CjhWe3ParJhz_g',
		client_secret = 'oG1mUr9L8OAfh-YM6HOxCaeimO0',
		username = 'edohub',
		password = 'hubedo123321',
		user_agent = 'edohubv1')

	subreddit = reddit.subreddit(subreddit)
	new_submissions = subreddit.new(limit=5)

	return new_submissions