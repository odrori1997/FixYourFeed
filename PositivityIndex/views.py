from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Twitter,Index
from django.contrib.auth.models import User
from django.template import loader
from django.shortcuts import get_object_or_404, get_list_or_404, render, resolve_url, redirect
from . import apps
from PositivityIndex import indexcalc
from django.views import generic
from django.urls import reverse
# 	from django.shortcuts import render
# from django.contrib.auth import views as auth_views
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import get_object_or_404, get_list_or_404, render, resolve_url, redirect


def index(request):
	user = request.user
	twitter = Twitter.objects.filter(user=user)
	index_list = Index.objects.filter(twitter=twitter).order_by('run_date')[:5]
	return render(request, 'PositivityIndex/index.html', {
		'twitter': twitter,
		'index_list': index_list
		})


def results(request):
	user = request.user
	if request.method == 'POST':
		search_user = request.POST.get('textfield', None)
		indexcalc.display_result(search_user, False)
	else: # add functionality to analyze your own feed here
		try:
			search_user = Twitter.objects.filter(user=user)
		except Twitter.DoesNotExist:
			raise Http404

		try:
			search_user = search_user[0].name
		except IndexError:
			raise Http404

	# return all indices associated with twitter handle search_user
	try:
		twitter = Twitter.objects.filter(name=search_user)
	except Twitter.DoesNotExist:
		raise Http404
	twitter = twitter[0]
	try:
		index_list = Index.objects.filter(twitter=twitter)
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

