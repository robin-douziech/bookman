from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import models


class BookSearchForm(forms.Form):

    search_txt = forms.CharField(
        label="Search text",
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Search for a book'})
    )

    def __init__(self, request, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.fields['search_txt'].initial = request.GET.get('search', '')


class AuthorCreationForm(forms.Form):

    first_name = forms.CharField(
        label="First name",
        max_length=20
    )

    last_name = forms.CharField(
        label="Last name",
        max_length=20
    )

    def clean(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        for author in models.Author.objects.all():
            if author.first_name == first_name and author.last_name == last_name:
                raise ValidationError(
                    _("Author %(author)s already registered in database"),
                    params={'author': f"{first_name} {last_name}"}
                )
        return self.cleaned_data


class PublisherCreationForm(forms.Form):

    name = forms.CharField(
        label="Name",
        max_length=50
    )

    def clean(self):
        name = self.cleaned_data['name']
        for publisher in models.Publisher.objects.all():
            if publisher.name == name:
                raise ValidationError(
                    _("Publisher %(publisher)s already registered in database"),
                    params={'publisher': name}
                )
        return self.cleaned_data


class GenreCreationForm(forms.Form):

    name = forms.CharField(
        label="Name",
        max_length=50
    )

    def clean(self):
        name = self.cleaned_data['name']
        for genre in models.Genre.objects.all():
            if genre.name == name:
                raise ValidationError(
                    _("Genre %(genre)s already registered in database"),
                    params={'genre': name}
                )
        return self.cleaned_data


class BookCreationForm(forms.Form):

    title = forms.CharField(
        label="Title",
        max_length=50
    )

    author = forms.ModelChoiceField(
        label="Author",
        queryset=models.Author.objects.all()
    )

    publisher = forms.ModelChoiceField(
        label="Publisher",
        queryset=models.Publisher.objects.all()
    )

    genre = forms.ModelChoiceField(
        label="Genre",
        queryset=models.Genre.objects.all()
    )

    front_cover = forms.ImageField(
        label="Front cover"
    )

    back_cover = forms.ImageField(
        label="Back cover"
    )

    def clean(self):
        title = self.cleaned_data['title']
        author = self.cleaned_data['author']
        for book in models.Book.objects.all():
            if book.title == title and book.author == author:
                raise ValidationError(
                    _("Book \"%(book)s\" by %(author)s already registered in database"),
                    params={'book': title, 'author': author}
                )
        return self.cleaned_data
