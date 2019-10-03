from . import views
from django.urls import include, path


urlpatterns = [
	path('index', views.index, name='index'),
	path('<int:index_id>/', views.index, name='index'),
	path('<int:index_id>/results', views.results, name='results'),
	path('results', views.results, name='results'),
]