from django.urls import path

from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('<int:index_id>/', views.results, name='results'),
	path('<int:index_id>/results', views.results, name='results'),
	path('results', views.results, name='results'),
	path('loading', views.loading, name='loading'),
]