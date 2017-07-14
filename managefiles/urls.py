from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
	url(r'^home/$', views.file_upload, name='file_upload'),
]
