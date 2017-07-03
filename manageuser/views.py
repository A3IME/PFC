from django.shortcuts import render, redirect
from django.http import HttpResponse

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
	print(request.POST)
	return render(request, 'manageuser/login.html')
