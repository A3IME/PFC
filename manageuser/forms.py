from django import forms

class Login(forms.Form):
	username = forms.CharField(label='Usuário', error_messages={'required': 'Usuário não informado'})
	password = forms.CharField(label='Senha', widget=forms.PasswordInput, error_messages={'required': 'Senha não informada'})

class Register(forms.Form):
	name  = forms.CharField(label = 'Nome', required = False)
	surname  = forms.CharField(label = 'Sobrenome', required = False)
	username_register = forms.CharField(label='Usuário', error_messages={'required': 'Usuário não informado'})
	password_register = forms.CharField(label='Senha', widget=forms.PasswordInput, error_messages={'required': 'Senha não informada'})
	cpassword = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput, error_messages={'required': 'Confirmação de senha não informada'})

	email = forms.CharField(label='Email', widget=forms.EmailInput, error_messages={'required': 'Email não informado'})

class Update_infos(forms.Form):
	name  = forms.CharField(label = 'Nome', required = False)
	surname  = forms.CharField(label = 'Sobrenome', required = False)

	email = forms.CharField(label='Email', widget=forms.EmailInput, error_messages={'required': 'Email não informado'})

class Change_password(forms.Form):
	password = forms.CharField(label='Senha', widget=forms.PasswordInput, error_messages={'required': 'Senha não informada'})
	newPassword = forms.CharField(label='Nova senha', widget=forms.PasswordInput, error_messages={'required': 'Nova senha não informada'})
	cnewPassword = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput, error_messages={'required': 'Confirmação de nova senha não informada'})
