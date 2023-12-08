from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import models

class LoginForm(forms.Form) :

	username = forms.CharField(
		label="Username",
		max_length=50
	)

	password = forms.CharField(
		label="Password",
		max_length=50,
		widget=forms.PasswordInput()
	)

class UserCreationForm(forms.Form) :

	username = forms.CharField(
		label="Username",
		max_length=50
	)

	password1 = forms.CharField(
		label="Password",
		max_length=50,
		widget=forms.PasswordInput()
	)

	password2 = forms.CharField(
		label="Confirm password",
		max_length=50,
		widget=forms.PasswordInput()
	)

	email = forms.EmailField(label="Email")

	def clean(self) :
		username = self.cleaned_data['username']
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']
		email = self.cleaned_data['email']

		for user in models.User.objects.all() :
			if user.username == username :
				raise ValidationError(_("Username %(username)s already used."), params={"username": username})
			elif user.email == email :
				raise ValidationError(_("E-mail %(email)s already used."), params={"email": email})
		if password1 != password2 :
			raise ValidationError(_("Entered password differ."))

		return self.cleaned_data



