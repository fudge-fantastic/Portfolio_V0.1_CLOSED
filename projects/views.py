# views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from projects.forms import ContactForm
from projects.models import ContactMessage
from django.conf import settings
from django.contrib import messages
import os

# NavBar
def index(request):
    return render(request, "index.html")

def about(request): 
    return render(request, "about.html")

def projects(request):
    return render(request, "projects.html")

def connect(request):
    return render(request, "connect.html")

# Projects Pages
def machine_learning(request):
    return render(request, "machine_learning/machine_learning.html")

def deep_learning(request):
    return render(request, "deep_learning/deep_learning.html")

def generative_ai(request):
    return render(request, "generative_ai/generative_ai.html")

def resume_analyzer(request):
    return render(request, "generative_ai/resume_analyzer.html")

# Contact Form
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Example: Sending email
            send_mail(
                'Message from the Portfolio page',
                f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # Add a success message
            messages.success(request, 'Your message has been sent successfully! Now Shooo...!!')

            # Redirect to a different URL (PRG pattern)
            return redirect('contact')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})