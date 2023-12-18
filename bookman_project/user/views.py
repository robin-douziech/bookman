from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login

from bookman import helpers
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
    return render(request, 'user/creation.html', {
        'form': form
    })

@login_required
@helpers.select_user
def details(request, selected_user=None):

    username = request.GET.get('user', False)
    if username:
        try:
            user = models.User.objects.get(username=username)
        except:
            user = None
        if user is not None and admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user):
            return render(request, 'user/detail.html', {
                'page_user': user,
                'selected_user': selected_user
            })
        else:
            return redirect('/')
    else:
        return redirect('/')

@login_required
@helpers.select_user
def list(request, selected_user=None):
    if request.user.is_librarian:
        search_txt = request.GET.get('search', False)
        form = forms.UserSearchForm(request, request.GET)
        if form.is_valid():
            results = models.User.objects.filter(
                username__contains=form.cleaned_data['search_txt'])
        return render(request, 'user/list.html', {
            'form': form,
            'results': results,
            'selected_user': selected_user
        })
    else:
        return redirect('/')

@login_required
@helpers.user_is_librarian
@helpers.select_user
def select_user(request, selected_user=None) :
    user_id = request.GET.get('id', False)
    if user_id :
        try :
            user = models.User.objects.get(pk=user_id)
            return redirect(f"{reverse('user:details')}?id={user_id}&select={user_id}")
        except :
            return redirect(f"{reverse('user:details')}?id={user_id}")
    else :
        return redirect('/')

@login_required
@helpers.user_is_librarian
@helpers.select_user
def unselect_user(request, selected_user=None) :
    selected_user_id = request.GET.get('select', False)
    if selected_user_id :
        try :
            user = models.User.objects.get(pk=selected_user_id)
            return redirect(f"{reverse('user:details')}?id={selected_user_id}")
        except :
            return redirect('/')
    else :
        return redirect('/')

