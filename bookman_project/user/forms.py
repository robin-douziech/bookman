from django import forms

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