from collections import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import praw
import urllib
from bs4 import BeautifulSoup

def index(request):

	if not request.user.is_authenticated():
		return redirect('/accounts/login/')

	weather = temperature()
	rkpop_posts = reddit('kpop')
	rtwice_posts = reddit('twice')

	sfg_traderumors = traderumors();

	content = {'username': request.user.username, 'temp': weather, 'rkpop_posts': rkpop_posts, 'rtwice_posts': rtwice_posts, 'sfg_traderumors': sfg_traderumors}
	#content = {'username': request.user.username, 'temp': weather, 'sfg_traderumors': sfg_traderumors}

	return render(request, 'hub/home.html', content)


def temperature():
	zipcode = '94122'
	r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=d7608eb9909f2561fa7a7a1b62d078b5')
	temp_k = float(r.json()['main']['temp'])
	temp_f = int(round((temp_k - 273) * 1.8 + 32))
	return temp_f

def reddit(subreddit, limit = 5):
	reddit = praw.Reddit(client_id = 'CjhWe3ParJhz_g',
		client_secret = 'oG1mUr9L8OAfh-YM6HOxCaeimO0',
		username = 'edohub',
		password = 'hubedo123321',
		user_agent = 'edohubv1')

	subreddit = reddit.subreddit(subreddit)
	new_submissions = subreddit.new(limit=limit)

	return new_submissions

def traderumors():
	target_page = 'https://www.mlbtraderumors.com/san-francisco-giants'
	page = urllib.request.urlopen(target_page).read()
	soup = BeautifulSoup(page, 'html.parser')

	articles = OrderedDict()
	for data in soup.find_all('h2', class_='entry-title')[:5]:
		for a in data.find_all('a'):
			articles[a.text] = a['href'] 

	return articles