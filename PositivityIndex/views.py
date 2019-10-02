from django.http import HttpResponse
from .models import User,Index
from django.template import loader
from django.shortcuts import get_object_or_404, get_list_or_404, render
from . import apps
from PositivityIndex import indexcalc

def index(request):
	user_list = User.objects.all()
	return render(request, 'PositivityIndex/index.html', {'user': user_list})

def loading(request, index_id):
	return HttpResponse("You are currently loading index %s." % index_id)

def results(request):
	if request.method == 'POST':
		search_user = request.POST.get('textfield', None)
		indexcalc.display_result(search_user, False)
	user = get_object_or_404(User, name="@benshapiro")
	index_list = get_list_or_404(Index, user=user)
	# if (request.POST)
	# 	apps(index_id)
	return render(request, 'PositivityIndex/results.html', {
					'index': index_list,
					'user': user
					})

