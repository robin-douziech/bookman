from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("list", views.list, name="list"),
    path("details", views.details, name="details"),
    path("creation", views.user_creation, name="user_creation")
]
