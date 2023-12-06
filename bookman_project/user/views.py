from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login

from . import forms, models

def login_view(request) :

	error = {
		'errors_nb': 0,
		'wrong_password': [False, "The username/password couple you entered does not match"]
	}

@login_required
def logout_view(request) :
	logout(request)
	return redirect('/')

def user_creation(request) :

	form = forms.UserCreationForm()
	errors = {
		'errors_nb': 0,
		'passwords_missmatch': [False, "The two password you entered are different"]
	}

	if request.method == "POST" :
		form = forms.UserCreationForm(request.POST)
		if form.is_valid() :
			if form.cleaned_data['password1'] != form.cleaned_data['password2'] :
				errors['passwords_missmatch'][0] = True
				errors['errors_nb'] += 1
			if errors['errors_nb'] == 0 :
				user = models.User.objects.create_user(
					form.cleaned_data['username'],
					form.cleaned_data['email'],
					form.cleaned_data['password1']
				)
				user.save()
				return redirect('/')

	errors.pop('errors_nb')
	return render(request, 'user/creation.html', {'form': form, 'errors': errors})
