from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def my_login_required(function=None, login_url=None):
	actual_decorator = login_required(function=function, redirect_field_name=None, login_url=login_url)
	return actual_decorator

def my_anonymous_required(func):
	def func_wrapper(request):
		if not request.user.is_authenticated():
			return func(request)
		else:
			return redirect('/')
	return func_wrapper


def my_create_user(form, request):
	username = form.cleaned_data['username']
	password = form.cleaned_data['password']
	email = form.cleaned_data['email']
	name = form.cleaned_data['name']
	surname = form.cleaned_data['surname']

	user = User.objects.create_user(username, email, password)
	user.first_name = name
	user.last_name = surname
	user.save()

	###
	#CREATE DIRECTORY STRUCTURE HERE
	###
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
	
	return redirect('/')


def my_update_info_user(form, request):
	request.user.email = form.cleaned_data['email']
	request.user.first_name = form.cleaned_data['name']
	request.user.last_name = form.cleaned_data['surname']
	request.user.save()

#def user_to_form(user):
	
