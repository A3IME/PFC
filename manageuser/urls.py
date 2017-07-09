from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	url(r'^login/$', views.login, name='login'),
	url(r'^registrar/$', views.register, name='register'),
	url(r'^atualizar/$', views.update_infos, name='update_infos'),
	url(r'^novasenha/$', views.change_password, name='change_password'),
	url(r'^logout/$', views.logout, name='logout'),
]
