from django.urls import path

from . import views

app_name = "book"
urlpatterns = [
    path("", views.index, name="index"),
    path("details/", views.details, name="details"),
    path("new-author", views.author_creation, name="author_creation"),
    path("new-publisher", views.publisher_creation, name="publisher_creation"),
    path("new-genre", views.genre_creation, name="genre_creation"),
    path("new-book", views.book_creation, name="book_creation"),
    path("my-books", views.user_books_view, name="user_books_view"),
    path('rent_book/', views.rent_book, name='rent_book'),
    path('recognition/', views.recognition, name='recognition'),
    path('manage/<int:book_id>/', views.manage_books, name='manage'),
    path('return_book/', views.return_book, name='return_book'),
]
