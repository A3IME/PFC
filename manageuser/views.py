from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
	if request.user.is_authenticated():
		return HttpResponse("<h2>FUNCIONA AUTHENTICATION</h2>")
	else:
		return redirect('/login/')

def register(request):
	return HttpResponse("<h2>FUNCIONA REGISTER</h2>")

def login(request):
	return HttpResponse("<h2>FUNCIONA LOGIN</h2>")
