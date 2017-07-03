from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

def index(request):
	if request.user.is_authenticated():
		return HttpResponse("<h2>FUNCIONA AUTHENTICATION</h2>")
	else:
		return redirect('/login/')

def register(request):
	return render(request, 'manageuser/register.html')
#	if request.POST == None:
#		return HttpResponse("<h2>FUNCIONA REGISTER NONE</h2>")
#	else:
#		return HttpResponse("<h2>FUNCIONA REGISTER NOT NONE</h2>")

def login(request):
	if request.method == 'POST':
		print("test post")
		print(request.POST)
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return HttpResponse("<h2>USER OK</h2>")
		else:
			return render(request, 'manageuser/login.html', request.POST)
	else:
		return render(request, 'manageuser/login.html')
