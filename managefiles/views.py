from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from .forms import File_upload, UploadFileForm
from src.definitions import my_login_required, save_uploaded_file
import subprocess
from subprocess import check_output
from pathlib import Path
from distutils.dir_util import copy_tree
import os
import json
from json2html import *
import requests

@my_login_required
def file_upload(request):
	if request.method == 'POST':
		form = File_upload(request.POST, request.FILES)
		if form.is_valid():
			save_uploaded_file(request.user, request.FILES['file'])
			return redirect("managefiles:show_directories")
	else:
		form = File_upload()
	return render(request, 'managefiles/fileform.html', {'form': form, 'headCode': '<title>Início</title>', 'submitValue': 'Enviar'})


@my_login_required
def show_directories(request):
	user = request.user
	reports_directory = check_output(["pwd"]).decode("utf-8")[:-1] + "/usr/" + user.directories.directory
	user_directories_list = check_output(["ls", reports_directory]).decode("utf-8").split("\n")
	user_directories_list.pop()
	info_list = []
	for directory in user_directories_list:
	    ls = subprocess.Popen(('ls', reports_directory + "/" + directory), stdout=subprocess.PIPE)
	    output = subprocess.check_output(('grep', '-v', 'reports'), stdin=ls.stdout).decode("utf-8").split("\n")[0]
	    ls.wait()
	    ready_reports = check_output(["ls", reports_directory + "/" + directory + "/reports"]).decode("utf-8").split("\n")
	    info_list.append({"dir":directory, "file":output, "virus_total_ready":"virus_total.json" in ready_reports, "static_ready":"static_analysis.json" in ready_reports, "dynamic_ready":"Arquivos_Analise_Dinamica.zip" in ready_reports})

	return render(request, 'managefiles/relatorios.html', {'user_name': user.username, 'info_list': info_list})

@my_login_required
def show_reports(request, report_time):
	return render(request, 'managefiles/reports.html', {'user_name': request.user.username, 'report_time': report_time})

def download_file(request, report_time, analysis_type, view_method):
	user = request.user
	dir_path = check_output(["pwd"]).decode("utf-8")[:-1] + "/usr/" + user.directories.directory + "/" + report_time + "/reports"

	if view_method == "json":
                if (analysis_type == "static_analysis") or (analysis_type == "virus_total"):
	                with open(dir_path + "/" + analysis_type + ".json", "r") as f:
                                response = HttpResponse(f.read(), content_type="json")
                                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(dir_path + "/" + analysis_type + ".json")
                                return response
                elif analysis_type == "dynamic_analysis":
                        with open(dir_path + "/Arquivos_Analise_Dinamica.zip", "rb") as f:
                                response = HttpResponse(f.read(), content_type="application/zip")
                                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(dir_path + "/Arquivos_Analise_Dinamica.zip")
                                return response		
	else:
		if (analysis_type != "dynamic_analysis"):
			with open(dir_path + "/" + analysis_type + ".json", "r") as f:
				content = f.read()
			return HttpResponse(content)
		else:
			with open(dir_path + "/dynamic_analysis.html", "r") as f:
				content = f.read()
			return HttpResponse(content)
	raise Http404


def make_response(status=200, content_type='text/plain', content=None):
	response = HttpResponse()
	response.status_code = status
	response['Content-Type'] = content_type
	response.content = content
	redirect("managefiles:show_directories")
	return response

@my_login_required
def home(request):
	return render(request, 'managefiles/forms_file_uploader.html')


class UploadView(TemplateView):
	@csrf_exempt
	def dispatch(self, *args, **kwargs):
		return super(UploadView, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			save_uploaded_file(request.user, request.FILES['qqfile'])
			return make_response(content=json.dumps({ 'success': True }))
		else:
			return make_response(status=400, content=json.dumps({
					'success': False,
					'error': '%s' % repr(form.errors)
				}))


