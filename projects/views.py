# Create your views here.
from django.shortcuts import render
import os

def index(request):
    return render(request, "index.html")

def about(request): 
    return render(request, "about.html")

def projects(request):
    return render(request, "projects.html")

def contact(request):
    return render(request, "contact.html")
