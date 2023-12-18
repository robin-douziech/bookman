from django.urls import path

from . import views

app_name = "book"
urlpatterns = [
    path("", views.index, name="index"),
    path("details", views.details, name="details"),

    path("new-author", views.author_creation, name="author_creation"),
    path("new-publisher", views.publisher_creation, name="publisher_creation"),
    path("new-genre", views.genre_creation, name="genre_creation"),
    path("new-book", views.book_creation, name="book_creation"),

    path("add-copie", views.add_copie, name="add_copie"),
    path("del-copie", views.del_copie, name="del_copie"),
    path("rent", views.rent_book, name="rent_book"),
    path("give-back", views.give_book_back, name="give_book_back")
]
