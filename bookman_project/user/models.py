from django.db import models
from django.contrib.auth.models import AbstractUser
from book.models import Book


class User(AbstractUser):

    is_librarian = models.BooleanField(default=False)
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.username
