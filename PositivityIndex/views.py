from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Twitter,Index
from django.contrib.auth.models import User
from django.template import loader
from django.shortcuts import get_object_or_404, get_list_or_404, render, resolve_url, redirect
from . import apps
from PositivityIndex import indexcalc
from django.views import generic
from django.urls import reverse
from social_django.models import UserSocialAuth
# 	from django.shortcuts import render
# from django.contrib.auth import views as auth_views
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import get_object_or_404, get_list_or_404, render, resolve_url, redirect

def userhome(request):
	user = request.user
	return render(request, 'userhome.html', {
		'user': user
		})

def guesthome(request):
	return render(request, 'guesthome.html')


def index(request):
	user = request.user
	index_list = Index.objects.filter(user=user).order_by('run_date')[:5]
	Dict = {}
	for i in index_list:
		Dict[i] = i.run_date.strftime('%Y-%m-%d')
		print(i.run_date.strftime('%Y-%m-%d'))
	return render(request, 'PositivityIndex/index.html', {
		'user': user,
		'index_list': index_list,
		'Dict': Dict
		})


def results(request):
	user = request.user
	if request.method == 'POST':
		search_user = request.POST.get('textfield', None)
		if request.POST.get('textfield', None) == None:
			indexcalc.display_result(search_user, True)
		else:
			indexcalc.display_result(search_user, False)
	else: # add functionality to analyze your own feed here
		try:
			twitter_login = user.social_auth.get(provider='twitter')
		except UserSocialAuth.DoesNotExist:
			twitter_login = None
		if twitter_login != None:
			search_user = user.username
			indexcalc.display_result(search_user, True)
		else:
			search_user = None


	# return all indices associated with twitter handle search_user
	try:
		twitter = Twitter.objects.filter(name=search_user)
	except Twitter.DoesNotExist:
		raise Http404
	twitter = twitter[0]
	try:
		index_list = Index.objects.filter(twitter=twitter).order_by('run_date')[0]
	except Index.DoesNotExist:
		index_list = None
	# if (request.POST)
	# 	apps(index_id)
	return render(request, 'PositivityIndex/results.html', {
					'index': index_list,
					'user': user
					})

# def signup(request):
# 	if request.method == 'POST':
# 		form = UserCreationForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data.get('username')
# 			raw_password = form.cleaned_data.get('password1')
# 			user = authenticate(username = username, password = raw_password)
# 			login(request, user)
# 			return redirect('home')


# def LoginView(request):
# 	template_name = 'registration/login.html'
# 	username = request.POST['username']
# 	password = request.POST['password']
# 	user = authenticate(request, username = username, password = password)
# 	if user is not None:
# 		login(request, user)
# 		redirect('PositivityIndex/index.html', user)
# 	else:
# 		# return invalid login error message
# 		redirect('PositivityIndex/loading.html')

