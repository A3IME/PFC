from django.conf.urls import url
from django.views.generic import RedirectView
from . import views
from managefiles.views import UploadView

app_name = "managefiles"
urlpatterns = [
	url(r'^home/$', views.home, name='home'),
    url(r'^test/', views.home, name='test'),
    url(r'^up(?:/(?P<qquuid>\S+))?', UploadView.as_view(), name='upload'),
    url(r'^relatorios/$', views.show_directories, name='show_directories'),
    url(r'^relatorios/(?P<report_time>([0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{6}))/$', views.show_reports, name='show_reports'),
    url(r'^relatorios/(?P<report_time>([0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{6}))/(?P<analysis_type>((static_analysis)|(dynamic_analysis)|(virus_total)))/(?P<view_method>((html)|(json)))/$', views.download_file, name='download'),
]
