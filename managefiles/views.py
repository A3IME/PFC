from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import File_upload, UploadFileForm
from src.definitions import my_login_required, save_uploaded_file
import subprocess
from subprocess import check_output
from pathlib import Path
from distutils.dir_util import copy_tree
import os
import json
import requests

@my_login_required
def file_upload(request):
	if request.method == 'POST':
		print("UP POST")
		form = File_upload(request.POST, request.FILES)
		print(request.POST)
		print(request.FILES)
		if form.is_valid():
			print("UP VALID")
			save_uploaded_file(request.user, request.FILES['file'])
			return redirect("managefiles:show_directories")
	else:
		form = File_upload()
		print(request.FILES)
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
	    print(ready_reports)
	    info_list.append({"dir":directory, "file":output, "virus_total_ready":"virus_total.json" in ready_reports, "static_ready":"static_analysis.json" in ready_reports, "dynamic_ready":"Arquivos_Analise_Dinamica.zip" in ready_reports})

	return render(request, 'managefiles/relatorios.html', {'user_name': user.username, 'info_list': info_list})

@my_login_required
def show_reports(request, report_time):
# Criar lógica de fornecer arquivos para baixar aqui
	print(report_time)
	return render(request, 'managefiles/reports.html', {'user_name': request.user.username, 'report_time': report_time})

def download_file(request, report_time, analysis_type):
	user = request.user
	dir_path = check_output(["pwd"]).decode("utf-8")[:-1] + "/usr/" + user.directories.directory + "/" + report_time + "/reports"
	if analysis_type == "static":
		with open(dir_path + "/static_analysis.json", "r") as f:
			response = HttpResponse(f.read(), content_type="json")
			response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(dir_path + "/static_analysis.json")
			return response
	elif analysis_type == "dynamic":
		"""		
		dir_dynamic_files = dir_path + "/dynamic_files"
		with open(dir_path + "/id_cuckoo.json", "r") as f:
			id_cuckoo = f.read()
		r = requests.get("http://localhost:8090/tasks/view/" + id_cuckoo)
		status = r.json()["task"]["status"]

		if status == 'reported':
			fromDirectory = "/home/artefathos/.cuckoo/storage/analyses/" + id_cuckoo
			toDirectory = dir_path + "/dynamic_files"
			copy_tree(fromDirectory, toDirectory)
		with open(dir_dynamic_files + "/reports/report.json", "r") as f:
			response = HttpResponse(f.read(), content_type="json")
			response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(dir_path + "/dynamic_analysis.json")
		"""
		with open(dir_path + "/Arquivos_Analise_Dinamica.zip", "r") as f:
			response = HttpResponse(f.read(), content_type="zip")
			response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(dir_path + "/dynamic_analysis.zip")
			return response		
	elif analysis_type == "virus_total":
		with open(dir_path + "/virus_total.json", "r") as f:
			response = HttpResponse(f.read(), content_type="json")
			response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(dir_path + "/virus_total.json")
			return response
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
			#handle_upload(request.FILES['qqfile'], form.cleaned_data)
			save_uploaded_file(request.user, request.FILES['qqfile'])
			return make_response(content=json.dumps({ 'success': True }))
		else:
			return make_response(status=400, content=json.dumps({
					'success': False,
					'error': '%s' % repr(form.errors)
				}))


