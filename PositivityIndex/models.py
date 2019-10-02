from django.db import models

class User(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Index(models.Model):
	run_date = models.DateTimeField('date analyzed')
	positive_tweets = models.IntegerField(default=0)
	negative_tweets = models.IntegerField(default=0)
	neutral_tweets = models.IntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.name