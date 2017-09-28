from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import Login, Register, Update_infos, Change_password
from src.definitions import my_login_required, my_anonymous_required, my_create_user, my_update_info_user, my_change_password
from django.contrib.auth.models import User


@my_anonymous_required
def index(request):
    if 'Registrar' in request.POST:
        return register(request)
    else:
        return login(request)


# @my_anonymous_required
def register(request):
    form_login = Login()
    if request.method == 'POST':
        #print(request.POST)
        form_register = Register(request.POST)

        if form_register.is_valid():
            if User.objects.filter(username=form_register.cleaned_data['username_register']).exists():
                form_register.add_error('username_register', 'Usuário já existe.')
            elif form_register.cleaned_data['password_register'] != form_register.cleaned_data['cpassword']:
                form_register.add_error('cpassword', 'Senha e confirmação diferentes')
            else:
                my_create_user(form_register, request)
                return redirect('/')
    else:
        form_register = Register()
    return render(request, 'manageuser/test.html',
                  {'form_register': form_register, 'form_login': form_login, 'headCode': '<title>Cadastro</title>',
                   'submitValue': 'Registrar'})


# @my_anonymous_required
def login(request):
    form_register = Register()
    if request.method == 'POST':
        form_login = Login(request.POST)

        if form_login.is_valid():
            user = authenticate(username=form_login.cleaned_data['username'],
                                password=form_login.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:
                form_login.add_error(None, 'Usuário ou senha incorretos.')
    else:
        form_login = Login()
    return render(request, 'manageuser/test.html',
                  {'form_login': form_login, 'form_register': form_register, 'headCode': '<title>Login</title>',
                   'submitValue': 'Entrar'})


@my_login_required
def update_infos(request):
    if request.method == 'POST':
        form = Update_infos(request.POST)
        if form.is_valid():
            my_update_info_user(form, request)
            return redirect('/')
    else:
        form = Update_infos(initial={

            'name': request.user.get_full_name().split()[0],
            'surname': request.user.get_full_name().split()[1],
            'email': request.user.email
        })
    return render(request, 'managefiles/atualizar_cadastro.html',
                  {'form': form, 'headCode': '<title>Atualizar</title>', 'submitValue': 'Atualizar'})


@my_login_required
def change_password(request):
    if request.method == 'POST':
        form = Change_password(request.POST)
        if form.is_valid():
            if not request.user.check_password(form.cleaned_data['password']):
                form.add_error('password', 'Senha incorreta')
            elif form.cleaned_data['newPassword'] != form.cleaned_data['cnewPassword']:
                form.add_error('cnewPassword', 'Nova senha e confirmação diferentes')
            else:
                my_change_password(form, request)
                return redirect('/')
    else:
        form = Change_password()
    return render(request, 'managefiles/nova_senha.html', {'form': form, 'headCode': '<title>Alterar senha</title>', 'submitValue': 'Alterar'})


@my_login_required
def logout(request):
    auth_logout(request)
    return redirect('/')
