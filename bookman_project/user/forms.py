from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator

from . import models


class LoginForm(forms.Form):

    username = forms.CharField(
        label="Username",
        max_length=50
    )

    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=forms.PasswordInput()
    )


class UserCreationForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Password",
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirm password",
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row='<p%(html_class_attr)s>%(label)s %(field)s%(help_text)s</p>',
            error_row='<div class="alert alert-danger" role="alert">%s</div>',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=False)

    def clean(self):
        username = self.cleaned_data['username']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        email = self.cleaned_data.get('email')

        error_messages = []
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            error_messages.append(_("Invalid email address."))

        for user in models.User.objects.all():
            if user.username == username:
                error_messages.append(_("Username %(username)s already used.") % {
                                      "username": username})
            elif user.email == email:
                error_messages.append(
                    _("Email %(email)s already used.") % {"email": email})
        if password1 != password2:
            error_messages.append(_("Entered password differ."))

        if error_messages:
            raise ValidationError(error_messages)

        return self.cleaned_data


class UserSearchForm(forms.Form):
    search_txt = forms.CharField(
        label="Search text",
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control rounded', type: 'search', 'placeholder': 'Search Users', })
    )

    def __init__(self, request, *args, **kwargs):
        super(UserSearchForm, self).__init__(*args, **kwargs)
        self.fields['search_txt'].initial = request.GET.get('search', '')
