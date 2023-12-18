from django.shortcuts import redirect
from book import models as book_models
from user import models as user_models

def user_is_librarian(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_librarian:
            return function(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper

def select_user(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_librarian :
            try :
                user_id = request.GET.get('select', False)
                user = user_models.User.objects.get(pk=user_id)
            except :
                user = None
        else :
            user = None
        return function(request, selected_user=user, *args, **kwargs)
    return wrapper

def get_book(function):
    def wrapper(request, *args, **kwargs):
        book_id = request.GET.get('id', False)
        if book_id :
            try :
                book = book_models.Book.objects.get(pk=book_id)
                return function(request, book=book, *args, **kwargs)
            except :
                return redirect('/')
        else :
            return redirect('/')
    return wrapper