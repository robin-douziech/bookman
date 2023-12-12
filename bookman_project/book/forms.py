from django import forms

from . import models

class BookSearchForm(forms.Form) :

	search_txt = forms.CharField(
		label = "Search text",
		max_length = 50,
		required = False
	)

	def __init__(self, request, *args, **kwargs) :
		super(BookSearchForm, self).__init__(*args, **kwargs)
		self.fields['search_txt'].initial = request.GET.get('search', '')

class AuthorCreationForm(forms.Form) :

	first_name = forms.CharField(
		label = "First name",
		max_length = 20
	)

	last_name = forms.CharField(
		label = "Last name",
		max_length = 20
	)

class PublisherCreationForm(forms.Form) :

	name = forms.CharField(
		label = "Name",
		max_length = 50
	)

class GenreCreationForm(forms.Form) :

	name = forms.CharField(
		label = "Name",
		max_length = 50
	)

class BookCreationForm(forms.Form) :

	title = forms.CharField(
		label = "Title",
		max_length = 50
	)

	author = forms.ModelChoiceField(
		label = "Author",
		queryset = models.Author.objects.all()
	)

	publisher = forms.ModelChoiceField(
		label = "Publisher",
		queryset = models.Publisher.objects.all()
	)

	genre = forms.ModelChoiceField(
		label = "Genre",
		queryset = models.Genre.objects.all()
	)

	front_cover = forms.ImageField(
		label = "Front cover"
	)

	back_cover = forms.ImageField(
		label = "Back cover"
	)