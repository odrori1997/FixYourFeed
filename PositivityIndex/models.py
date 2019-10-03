from django.db import models
from django.contrib.auth.models import User

class Twitter(models.Model):
	name = models.CharField(max_length=200, default="")
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.name

class Index(models.Model):
	run_date = models.DateTimeField('date analyzed')
	positive_tweets = models.IntegerField(default=0)
	negative_tweets = models.IntegerField(default=0)
	neutral_tweets = models.IntegerField(default=0)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	twitter = models.ForeignKey(Twitter, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.run_date)