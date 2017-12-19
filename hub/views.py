from collections import OrderedDict
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import requests, praw, urllib
from bs4 import BeautifulSoup
from hub.forms import WeatherSettingForm
from hub.models import WeatherSetting

class HubView(TemplateView):

	template_name = 'hub/home.html'

	def get(self, request):
		if not request.user.is_authenticated():
			return redirect('/accounts/login/')

		weather_data = WeatherSetting.objects.filter(user=request.user)
		if weather_data.exists():
			weather_data = weather_data.latest('date')
			weather = self.temperature(zipcode = weather_data.zipcode, unit = weather_data.unit)
			weather_form = WeatherSettingForm(initial = {'zipcode' : weather_data.zipcode, 'unit' : weather_data.unit})
		else:
			weather_form = WeatherSettingForm()
			weather = self.temperature()
		
		#rkpop_posts = self.reddit('kpop')
		#rtwice_posts = self.reddit('twice')
		sfg_traderumors = self.traderumors();

		#content = {'username': request.user.username, 'temp': weather, 'weather_form' : weather_form, 'rkpop_posts': rkpop_posts, 'rtwice_posts': rtwice_posts, 'sfg_traderumors': sfg_traderumors}
		content = {'username': request.user.username, 'temp': weather, 'weather_form' : weather_form, 'sfg_traderumors': sfg_traderumors}

		return render(request, self.template_name, content)

	def post(self, request):
		weather_form = WeatherSettingForm(request.POST)
		if weather_form.is_valid():
			weather_setting = weather_form.save(commit = False)
			weather_setting.user = request.user
			weather_setting.save()
			weather_zip = weather_form.cleaned_data['zipcode']
			weather_unit = weather_form.cleaned_data['unit']
			return redirect('/hub')

	def temperature(self, zipcode = 94122, unit = 'f'):

		r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+str(zipcode)+',us&appid=d7608eb9909f2561fa7a7a1b62d078b5')
		temp = float(r.json()['main']['temp'])
		if unit == 'f':
			temp = int(round((temp - 273) * 1.8 + 32))
		elif unit == 'c': 
			temp = int(round(temp - 273.15))

		return str(temp) + unit.capitalize()


	def reddit(self, subreddit, limit = 5):
		reddit = praw.Reddit(client_id = 'CjhWe3ParJhz_g',
			client_secret = 'oG1mUr9L8OAfh-YM6HOxCaeimO0',
			username = 'edohub',
			password = 'hubedo123321',
			user_agent = 'edohubv1')

		subreddit = reddit.subreddit(subreddit)
		new_submissions = subreddit.new(limit=limit)

		return new_submissions

	def traderumors(self):
		target_page = 'https://www.mlbtraderumors.com/san-francisco-giants'
		page = urllib.request.urlopen(target_page).read()
		soup = BeautifulSoup(page, 'html.parser')

		articles = OrderedDict()
		for data in soup.find_all('h2', class_='entry-title')[:5]:
			for a in data.find_all('a'):
				articles[a.text] = a['href'] 

		return articles