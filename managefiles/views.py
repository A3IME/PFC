from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import File_upload, UploadFileForm
from src.definitions import my_login_required, save_uploaded_file
from subprocess import check_output
import os
import json

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
	return render(request, 'managefiles/relatorios.html', {'user_name': user.username, 'user_directories': user_directories_list})

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
		with open(dir_path + "/dynamic_analysis.json", "r") as f:
			response = HttpResponse(f.read(), content_type="json")
			response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(dir_path + "/dynamic_analysis.json")
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


