from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login

from . import forms, models, admin


def login_view(request):
    form = forms.LoginForm()
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('/')
    return render(request, 'user/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def user_creation(request):
    form = forms.UserCreationForm()
    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = models.User.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password1']
            )
            user.save()
            return redirect('/')
    return render(request, 'user/creation.html', {'form': form})


@login_required
def details(request):
    username = request.GET.get('user', False)
    if username:
        try:
            user = models.User.objects.get(username=username)
        except:
            user = None
        if user is not None and admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user):
            if request.method == 'POST':
                book_id = request.POST.get('book_id')
                book = models.Book.objects.get(id=book_id)
                user.books.remove(book)
                book.check_availability()
            books = user.books.all()
            return render(request, 'user/detail.html', {'page_user': user, 'books': books})
        else:
            return redirect('/')
    else:
        return redirect('/')


@login_required
def list(request):
    if request.user.is_librarian:
        search_txt = request.GET.get('search', False)
        form = forms.UserSearchForm(request, request.GET)
        if form.is_valid():
            results = models.User.objects.filter(
                username__contains=form.cleaned_data['search_txt'])
        return render(request, 'user/list.html', {'form': form, 'results': results})
    else:
        return redirect('/')
