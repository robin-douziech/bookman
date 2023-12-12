from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . import models, forms


def user_is_librarian(function) :
	def wrapper(request, *args, **kwargs) :
		if request.user.is_librarian :
			return function(request, *args, **kwargs)
		else :
			return redirect('/')
	return wrapper

def index(request) :
	search_txt = request.GET.get('search', False)
	form = forms.BookSearchForm(request, request.GET)
	if form.is_valid() :
		results = models.Book.objects.filter(title__contains=form.cleaned_data['search_txt'])
	return render(request, 'book/index.html', {'form': form, 'results': results})

def details(request) :

	book_id = request.GET.get('id', False)
	if book_id :
		try :
			book = models.Book.objects.get(pk=book_id)
		except :
			book = None
		if book is not None :
			return render(request, 'book/details.html', {'book': book})
	else :
		return redirect('/')

@login_required
@user_is_librarian
def author_creation(request) :
	form = forms.AuthorCreationForm()
	if request.method == "POST" :
		form = forms.AuthorCreationForm(request.POST)
		if form.is_valid() :
			author = models.Author(
				first_name = form.cleaned_data['first_name'],
				last_name = form.cleaned_data['last_name']
			)
			author.save()
			return redirect('/')
	return render(request, 'book/author/creation.html', {'form': form})

@login_required
@user_is_librarian
def publisher_creation(request) :
	form = forms.PublisherCreationForm()
	if request.method == "POST" :
		form = forms.PublisherCreationForm(request.POST)
		if form.is_valid() :
			publisher = models.Publisher(name=form.cleaned_data['name'])
			publisher.save()
			return redirect('/')
	return render(request, 'book/publisher/creation.html', {'form': form})

@login_required
@user_is_librarian
def genre_creation(request) :
	form = forms.GenreCreationForm()
	if request.method == "POST" :
		form = forms.GenreCreationForm(request.POST)
		if form.is_valid() :
			genre = models.Genre(name=form.cleaned_data['name'])
			genre.save()
			return redirect('/')
	return render(request, 'book/genre/creation.html', {'form': form})

@login_required
@user_is_librarian
def book_creation(request):
	form = forms.BookCreationForm()
	if request.method == "POST" :
		form = forms.BookCreationForm(request.POST, request.FILES)
		if form.is_valid() :
			book = models.Book(
				title = form.cleaned_data['title'],
				author = form.cleaned_data['author'],
				publisher = form.cleaned_data['publisher'],
				genre = form.cleaned_data['genre'],
				front_cover = None,
				back_cover = None
			)
			book.save()
			book.front_cover = form.cleaned_data['front_cover']
			book.back_cover = form.cleaned_data['back_cover']
			book.save()
			return redirect('/')
	return render(request, 'book/creation.html', {'form': form})
