from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
	path("creation", views.user_creation, name="user_creation")	
]