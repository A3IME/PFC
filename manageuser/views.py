from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import Login, Register
from src.definitions import my_login_required

###
#MUDAR ISSO PRO OUTRO APP
###
@my_login_required
def index(request):
	#if request.user.is_authenticated():
		return HttpResponse("<h2>FUNCIONA AUTHENTICATION</h2>")
	#else:
	#	return redirect('/login/')

def register(request):
	form = Register()
	return render(request, 'manageuser/form.html', {'form': form, 'headCode': '<title>Cadastro</title>', 'submitValue': 'Cadastrar'})
#	if request.POST == None:
#		return HttpResponse("<h2>FUNCIONA REGISTER NONE</h2>")
#	else:
#		return HttpResponse("<h2>FUNCIONA REGISTER NOT NONE</h2>")

def login(request):
	if not request.user.is_authenticated():
		if request.method == 'POST':
			form = Login(request.POST)

			if form.is_valid():
				user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
				if user is not None:
					auth_login(request, user)
					return HttpResponse("<h2>USER OK</h2>")
				else: 
					form.add_error(None, 'Usuário ou senha incorretos.')
		else:
			form = Login()
		return render(request, 'manageuser/form.html', {'form': form, 'headCode': '<title>Login</title>', 'submitValue': 'Entrar'})
	else:
		return redirect('')
