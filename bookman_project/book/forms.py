from django import forms

from . import models


class BookSearchForm(forms.Form):

    search_txt = forms.CharField(
        label="Search text",
        max_length=50,
        required=False
    )

    def __init__(self, request, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.fields['search_txt'].initial = request.GET.get('search', '')


class AuthorCreationForm(forms.Form):

    first_name = forms.CharField(
        label="First name",
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter first name'})
    )

    last_name = forms.CharField(
        label="Last name",
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter last name'})
    )


class PublisherCreationForm(forms.Form):

    name = forms.CharField(
        label="Name",
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter publisher name'})
    )


class GenreCreationForm(forms.Form):

    name = forms.CharField(
        label="Name",
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter genre name'})
    )


class BookCreationForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter title'})
    )

    author = forms.ModelChoiceField(
        label="Author",
        queryset=models.Author.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    publisher = forms.ModelChoiceField(
        label="Publisher",
        queryset=models.Publisher.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    genre = forms.ModelChoiceField(
        label="Genre",
        queryset=models.Genre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    front_cover = forms.ImageField(
        label="Front cover",
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    back_cover = forms.ImageField(
        label="Back cover",
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
