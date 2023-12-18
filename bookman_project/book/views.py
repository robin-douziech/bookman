from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from bookman import helpers

from user import models as user_models
from . import models, forms

@helpers.select_user
def index(request, selected_user=None):
    search_txt = request.GET.get('search', False)
    form = forms.BookSearchForm(request, request.GET)
    if form.is_valid():
        results = models.Book.objects.filter(
            title__contains=form.cleaned_data['search_txt'])
    return render(request, 'book/index.html', {
        'form': form,
        'results': results,
        'selected_user': selected_user
    })

@helpers.select_user
@helpers.get_book
def details(request, book, selected_user=None):
    return render(request, 'book/details.html', {
        'book': book,
        'selected_user': selected_user
    })

@login_required
@helpers.user_is_librarian
@helpers.select_user
def author_creation(request, selected_user=None):
    form = forms.AuthorCreationForm()
    if request.method == "POST":
        form = forms.AuthorCreationForm(request.POST)
        if form.is_valid():
            author = models.Author(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            author.save()
            return redirect('/')
    return render(request, 'book/author/creation.html', {
        'form': form,
        'selected_user': selected_user
    })


@login_required
@helpers.user_is_librarian
@helpers.select_user
def publisher_creation(request, selected_user=None):
    form = forms.PublisherCreationForm()
    if request.method == "POST":
        form = forms.PublisherCreationForm(request.POST)
        if form.is_valid():
            publisher = models.Publisher(name=form.cleaned_data['name'])
            publisher.save()
            return redirect('/')
    return render(request, 'book/publisher/creation.html', {
        'form': form,
        'selected_user': selected_user
    })


@login_required
@helpers.user_is_librarian
@helpers.select_user
def genre_creation(request, selected_user=None):
    form = forms.GenreCreationForm()
    if request.method == "POST":
        form = forms.GenreCreationForm(request.POST)
        if form.is_valid():
            genre = models.Genre(name=form.cleaned_data['name'])
            genre.save()
            return redirect('/')
    return render(request, 'book/genre/creation.html', {
        'form': form,
        'selected_user': selected_user
    })


@login_required
@helpers.user_is_librarian
@helpers.select_user
def book_creation(request, selected_user=None):
    form = forms.BookCreationForm()
    if request.method == "POST":
        form = forms.BookCreationForm(request.POST, request.FILES)
        if form.is_valid():
            book = models.Book(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                publisher=form.cleaned_data['publisher'],
                genre=form.cleaned_data['genre'],
                front_cover=None,
                back_cover=None
            )
            book.save()
            book.front_cover = form.cleaned_data['front_cover']
            book.back_cover = form.cleaned_data['back_cover']
            book.save()
            return redirect('/')
    return render(request, 'book/creation.html', {
        'form': form,
        'selected_user': selected_user
    })

@login_required
@helpers.user_is_librarian
@helpers.select_user
@helpers.get_book
def add_copie(request, book, selected_user=None) :
    book.nb_copies_owned += 1
    book.save()
    return redirect(f"{reverse('book:details')}?id={book.id}")

@login_required
@helpers.user_is_librarian
@helpers.select_user
@helpers.get_book
def del_copie(request, book, selected_user=None) :
    book.nb_copies_owned -= 1
    book.save()
    return redirect(f"{reverse('book:details')}?id={book.id}")

@login_required
@helpers.user_is_librarian
@helpers.select_user
@helpers.get_book
def rent_book(request, book, selected_user=None) :
    if selected_user != None :
        book.nb_copies_available -= 1
        book.save()
        selected_user.rented_books.add(book)
        selected_user.save()
    return redirect(f"{reverse('book:details')}?id={book.id}")

@login_required
@helpers.user_is_librarian
@helpers.select_user
@helpers.get_book
def give_book_back(request, book, selected_user=None) :
    if selected_user != None :
        book.nb_copies_available += 1
        book.save()
        selected_user.rented_books.remove(book)
        selected_user.save()
    return redirect(f"{reverse('book:details')}?id={book.id}")