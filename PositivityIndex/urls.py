from . import views
from django.urls import include, path


urlpatterns = [
	path('index', views.index, name='index'),
	path('<int:index_id>/', views.index, name='index'),
	path('<int:index_id>/results', views.results, name='results'),
	path('results', views.results, name='results'),
	path('userhome', views.userhome, name='userhome'),
	path('', views.guesthome, name='guesthome'),
	path('guesthome', views.guesthome, name='guesthome'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('searchuser', views.searchuser, name='searchuser'),
]