from django.db import models
from django.contrib.auth.models import User

class WeatherSetting(models.Model):
	user = models.ForeignKey(User)
	zipcode = models.IntegerField()
	unit = models.CharField(max_length = 1)
