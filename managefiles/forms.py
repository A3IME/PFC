from django import forms

class File_upload(forms.Form):
	file = forms.FileField(label = "Arquivo")
	
