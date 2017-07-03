from django import forms

class Login(forms.Form):
	username = forms.CharField(label='Usuário', error_messages={'required': 'Usuário não informado'})
	password = forms.CharField(label='Senha', widget=forms.PasswordInput, error_messages={'required': 'Senha não informada'})

class Register(forms.Form):
	name  = forms.CharField(label = 'Nome', required = False)
	surname  = forms.CharField(label = 'Sobrenome', required = False)
	username = forms.CharField(label='Usuário', error_messages={'required': 'Usuário não informado'})
	password = forms.CharField(label='Senha', widget=forms.PasswordInput, error_messages={'required': 'Senha não informada'})
	cpassword = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)

	email = forms.CharField(label='Email', widget=forms.EmailInput, error_messages={'required': 'Email não informado'})
