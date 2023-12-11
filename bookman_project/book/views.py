from django.shortcuts import render
from django.http import HttpResponse

def index(request) :
	return HttpResponse("Here is the main page of the bookman application")
