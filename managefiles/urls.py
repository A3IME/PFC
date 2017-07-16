from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

app_name = "managefiles"
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^home/$', views.file_upload, name='file_upload'),
        url(r'^reports/$', views.show_directories, name='show_directories'),
        url(r'^reports/(?P<report_time>([0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{6}))$', views.show_reports, name='reports'),
]
