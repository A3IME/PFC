from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login, name='login'),
	url(r'^registrar/$', views.register, name='register'),
]
