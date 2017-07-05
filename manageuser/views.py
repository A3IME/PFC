from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import Login, Register, Update_infos
from src.definitions import my_login_required, my_anonymous_required, my_create_user
from django.contrib.auth.models import User

###
#MUDAR ISSO PRO OUTRO APP
###
@my_login_required
def index(request):
	return HttpResponse("<h2>FUNCIONA AUTHENTICATION</h2>")


@my_anonymous_required
def register(request):
	if request.method == 'POST':
		print(request.POST)
		form = Register(request.POST)
		
		if form.is_valid():
			if User.objects.filter(username=form.cleaned_data['username']).exists():
				form.add_error('username', 'Usuário já existe.')
			elif form.cleaned_data['password'] != form.cleaned_data['cpassword']:
				form.add_error('cpassword', 'Senha e confirmação diferentes')
			else:
				return my_create_user(form, request)
	else:
		form = Register()
	return render(request, 'manageuser/form.html', {'form': form, 'headCode': '<title>Cadastro</title>', 'submitValue': 'Cadastrar'})


@my_anonymous_required
def login(request):
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


@my_login_required
def update_infos(request):
	if request.method == 'POST':
		form = Update_infos(request.POST)
		#VALIDAR FORM AQUI
	else:
		form = Update_infos(initial={

						'name': request.user.get_full_name().split()[0],
						'surname': request.user.get_full_name().split()[1],
						'email': request.user.email
					})
	return render(request, 'manageuser/form.html', {'form': form, 'headCode': '<title>Atualizar</title>', 'submitValue': 'Atualizar'})
