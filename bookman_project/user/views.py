from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login

from . import forms, models

def login_view(request) :
	form = forms.LoginForm()
	if request.method == "POST" :
		form = forms.LoginForm(request.POST)
		if form.is_valid() :
			user = authenticate(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password']
			)
			if user is not None :
				login(request, user)
				return redirect('/')
	return render(request, 'user/login.html', {'form': form})


@login_required
def logout_view(request) :
	logout(request)
	return redirect('/')

def user_creation(request) :
	form = forms.UserCreationForm()
	if request.method == "POST" :
		form = forms.UserCreationForm(request.POST)
		if form.is_valid() :
			user = models.User.objects.create_user(
				form.cleaned_data['username'],
				form.cleaned_data['email'],
				form.cleaned_data['password1']
			)
			user.save()
			return redirect('/')
	return render(request, 'user/creation.html', {'form': form})
