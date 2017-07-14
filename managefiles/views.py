from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import File_upload
from src.definitions import my_login_required, save_uploaded_file

@my_login_required
def file_upload(request):
	if request.method == 'POST':
		print("UP POST")
		form = File_upload(request.POST, request.FILES)
		print(request.POST)
		print(request.FILES)
		if form.is_valid():
			print("UP VALID")
			save_uploaded_file(request.user, request.FILES['file'])
			return HttpResponse("<h2>UPLOAD OK</h2>")
	else:
		form = File_upload()
		print(request.FILES)
	return render(request, 'managefiles/fileform.html', {'form': form, 'headCode': '<title>Início</title>', 'submitValue': 'Enviar'})

