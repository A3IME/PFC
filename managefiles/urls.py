from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

app_name = "managefiles"
urlpatterns = [
	url(r'^home/$', views.file_upload, name='file_upload'),
        url(r'^relatorios/$', views.show_directories, name='show_directories'),
        url(r'^relatorios/(?P<report_time>([0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{6}))/$', views.show_reports, name='show_reports'),
        url(r'^relatorios/(?P<report_time>([0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{6}))/(?P<analysis_type>((static)|(dynamic)|(virus_total)))/$', views.download_file, name='download'),
]
