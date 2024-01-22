from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from user.models import User
from .models import Book
from .orb_recognition import extract_descriptors, compare_descriptors
from django.contrib import messages

from . import models, forms
import pickle
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from .nn_embeds import get_embedding, compare_embeddings


def user_is_librarian(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_librarian:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper


def index(request):
    search_txt = request.GET.get('search', False)
    form = forms.BookSearchForm(request, request.GET)
    if form.is_valid():
        results = models.Book.objects.filter(
            title__contains=form.cleaned_data['search_txt'])
    return render(request, 'book/index.html', {'form': form, 'results': results})


def details(request):
    book_id = request.GET.get('id', False)
    if book_id:
        try:
            book = models.Book.objects.get(pk=book_id)
        except:
            book = None
        if book is not None:
            position = book.position.split(',')
            return render(request, 'book/details.html', {'book': book, 'position': position})
    else:
        return redirect('/')


@login_required
@user_is_librarian
def author_creation(request):
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
    return render(request, 'book/author/creation.html', {'form': form})


@login_required
@user_is_librarian
def publisher_creation(request):
    form = forms.PublisherCreationForm()
    if request.method == "POST":
        form = forms.PublisherCreationForm(request.POST)
        if form.is_valid():
            publisher = models.Publisher(name=form.cleaned_data['name'])
            publisher.save()
            return redirect('/')
    return render(request, 'book/publisher/creation.html', {'form': form})


@login_required
@user_is_librarian
def genre_creation(request):
    form = forms.GenreCreationForm()
    if request.method == "POST":
        form = forms.GenreCreationForm(request.POST)
        if form.is_valid():
            genre = models.Genre(name=form.cleaned_data['name'])
            genre.save()
            return redirect('/')
    return render(request, 'book/genre/creation.html', {'form': form})


@login_required
@user_is_librarian
def book_creation(request):
    form = forms.BookCreationForm()
    if request.method == "POST":
        form = forms.BookCreationForm(request.POST, request.FILES)
        if form.is_valid():
            book = models.Book(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                publisher=form.cleaned_data['publisher'],
                genre=form.cleaned_data['genre'],
                copies_available=form.cleaned_data['copies_available'],
                position=form.cleaned_data['position'],
                front_cover=None,
                back_cover=None
            )
            book.save()
            book.front_cover = form.cleaned_data['front_cover']
            book.back_cover = form.cleaned_data['back_cover']
            book.save()
            book.check_availability()
            return redirect('/')
    return render(request, 'book/creation.html', {'form': form})


@login_required
def user_books_view(request):
    books = request.user.books.all()
    return render(request, 'book/user_books_view.html', {'books': books})


@login_required
@user_is_librarian
def rent_book(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        user.books.add(book)
        book.check_availability()
        return redirect('/')
    else:
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        book.check_availability()
        users = User.objects.all()
        parsed_position = book.position.split(',')
        return render(request, 'book/rent_book.html', {'book': book, 'users': users, 'parsed_position': parsed_position})


@login_required
@user_is_librarian
def return_book(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        user.books.remove(book)
        book.check_availability()
        return redirect('/')
    else:
        book_id = request.GET.get('book_id')
        book = Book.objects.get(id=book_id)
        book.check_availability()
        users = User.objects.filter(books=book)
        parsed_position = book.position.split(',')
        return render(request, 'book/return_book.html', {'book': book, 'users': users, 'parsed_position': parsed_position})


@login_required
@user_is_librarian
def recognition(request):
    if request.method == 'POST':

        # Get the uploaded image from the request
        uploaded_image = request.FILES.get('image')

        # Read the uploaded image using cv2
        image = cv2.imdecode(np.frombuffer(
            uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR)

        # PIL image for neural network
        pil_image = Image.open(uploaded_image)

        # Process the uploaded image to extract descriptors
        descriptors = extract_descriptors(image)

        # Get the embeddings for the uploaded image
        embedding = get_embedding(pil_image)

        books = Book.objects.all()
        matches = []
        for book in books:
            # Load the pickled descriptors for front cover and back cover
            front_cover_descriptors = pickle.loads(
                book.descriptor_front)
            back_cover_descriptors = pickle.loads(book.descriptor_back)

            # Compare descriptors with both the front cover and back cover

            front_cover_score = compare_descriptors(
                descriptors, front_cover_descriptors)
            back_cover_score = compare_descriptors(
                descriptors, back_cover_descriptors)

            # Load the pickled embeddings for front cover and back cover

            front_cover_embedding = pickle.loads(book.embed_front)
            back_cover_embedding = pickle.loads(book.embed_back)

            # Compare embeddings with both the front cover and back cover

            front_cover_nn_score = compare_embeddings(
                embedding, front_cover_embedding)
            back_cover_nn_score = compare_embeddings(
                embedding, back_cover_embedding)

            # Load embeddings for front cover and back cover

            front_cover_embedding = pickle.loads(book.embed_front)
            back_cover_embedding = pickle.loads(book.embed_back)

            # Store the book and its best score in the matches list

            best_score = max(front_cover_score, back_cover_score)
            best_nn_score = round(
                max(front_cover_nn_score, back_cover_nn_score) * 100, 2)
            matches.append((book.id, best_score, best_nn_score))

        # Sort the matches by score in descending order and take the top 5

        matches = [(Book.objects.get(id=match_id), orb_score, nn_score)
                   for match_id, orb_score, nn_score in matches]
        top_matches = sorted(matches, key=lambda x: x[1], reverse=True)[:5]
        return render(request, 'book/search_result.html', {'matches': top_matches})
    else:
        return render(request, 'book/recognition.html')


@login_required
@user_is_librarian
def edit(request, book_id):
    book = models.Book.objects.get(id=book_id)
    form = forms.BookEditForm(request.POST or None,
                              request.FILES or None, instance=book)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'book/edit.html', {'form': form, 'book': book})


def delete(request):
    book_id = request.GET.get('book_id')
    if request.method == 'POST':
        book = models.Book.objects.get(id=book_id)
        book.delete()
        return redirect('/')
    else:
        book = models.Book.objects.get(id=book_id)
        return render(request, 'book/delete.html', {'book': book})


@login_required
@user_is_librarian
def manage_books(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'book/manage.html', {'book': book})
