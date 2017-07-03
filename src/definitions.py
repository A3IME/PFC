from django.contrib.auth.decorators import login_required
def my_login_required(function=None, login_url=None):
	#print("======")
	#print(func)
	actual_decorator = login_required(function=function, redirect_field_name=None, login_url=login_url)
	return actual_decorator
