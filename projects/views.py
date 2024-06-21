# Create your views here.
from django.shortcuts import render
import os

def index(request):
    return render(request, "index.html")

def about(request): 
    return render(request, "about.html")

def projects(request):
    return render(request, "projects.html")

def connect(request):
    return render(request, "connect.html")

def machine_learning(request):
    return render(request, "machine_learning/machine_learning.html")

def deep_learning(request):
    return render(request, "deep_learning/deep_learning.html")

def generative_ai(request):
    return render(request, "generative_ai/generative_ai.html")
