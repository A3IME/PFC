from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from subprocess import call, check_output
from datetime import datetime, timezone, timedelta
from time import strftime

def my_login_required(function=None, login_url=None):
	actual_decorator = login_required(function=function, redirect_field_name=None, login_url=login_url)
	return actual_decorator

def my_anonymous_required(func):
	def func_wrapper(request):
		if not request.user.is_authenticated():
			return func(request)
		else:
			return redirect('/home')
	return func_wrapper


def my_create_user(form, request):
	username = form.cleaned_data['username_register']
	password = form.cleaned_data['password_register']
	email = form.cleaned_data['email']
	name = form.cleaned_data['name']
	surname = form.cleaned_data['surname']

	user = User.objects.create_user(username, email, password)
	user.first_name = name
	user.last_name = surname
	user.save()

	root_directory = check_output(["pwd"]).decode("utf-8")[:-1]
	user_full_path = root_directory + "/usr/" + user.directories.directory
	call(["mkdir", "-p", user_full_path])
	call(["touch", user_full_path + "/.gitignore"])
	call(["chmod", "+w", user_full_path + "/.gitignore"])
	gitignore_file = open(user_full_path + "/.gitignore", "w")
	gitignore_file.write("# Ignore everything in this directory\n*\n# Except this file\n!.gitignore")
	gitignore_file.close()

	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)


def my_update_info_user(form, request):
	request.user.email = form.cleaned_data['email']
	request.user.first_name = form.cleaned_data['name']
	request.user.last_name = form.cleaned_data['surname']
	request.user.save()

def my_change_password(form, request):
	username = request.user.get_username()
	password = form.cleaned_data['newPassword']

	user = User.objects.get(username__exact=request.user.get_username())
	user.set_password(form.cleaned_data['newPassword'])
	user.save()	

	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)

def save_uploaded_file(user, f):
	print("SAVE FILE")
	user_directory = check_output(['pwd']).decode("utf-8")[:-1] + "/usr/" + user.directories.directory + "/"
	full_path =  user_directory + datetime.now(tz=timezone(offset=timedelta(hours=-3))).strftime("%Y-%m-%d-%H-%M-%S-%f")
	call(["mkdir", "-p", full_path])
	call(["mkdir", "-p", full_path + "/reports"])
	gitignore_file = open(full_path + "/reports/.gitignore", "w")
	gitignore_file.write("# Ignore everything in this directory\n*\n# Except this file\n!.gitignore")
	gitignore_file.close()
	call(["rm", user_directory + ".gitignore"])
	file_path = full_path + "/" + f.name
	with open(file_path, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
	#CALL HERE MODEL 2 SCRIPT
	#FANTASY NAME FUNCTION BELOW
	generate_reports(full_path, file_path)

def generate_reports(full_path, file_path):
	generate_static_reports(full_path, file_path)
	generate_dynamic_reports(full_path, file_path)
	generate_virus_total_reports(full_path, file_path)
	print("SAVE FILE")

def generate_static_reports(full_path, file_path):
        static_analysis_string = check_output(["peframe", "--json", file_path]).decode("utf-8")
        strings_report_string = check_output(["peframe", "--strings", file_path]).decode("utf-8")
        final_string = "{\n\"analysis\":" + static_analysis_string[:-1] + ",\n\"strings\":" + strings_report_string + "}"
        with open(full_path + "/reports/static_analysis.json", "w+") as outputfile:
                outputfile.write(final_string)

#CHANGE THIS TO METHODS OF CLASSES
def generate_dynamic_reports(full_path, file_path):
        return

def generate_virus_total_reports(full_path, file_path):
        return
