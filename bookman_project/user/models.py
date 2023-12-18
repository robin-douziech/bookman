from django.db import models
from django.contrib.auth.models import AbstractUser

from book import models as book_models


class User(AbstractUser):

    is_librarian = models.BooleanField(default=False)

    rented_books = models.ManyToManyField(
        book_models.Book,
        blank = True,
        related_name = 'users_renting_the_book'
    )

    def __str__(self):
        return self.username
