## Instructions

When browser requests the URL, following steps are taken place:
- Django receives the URL, checks the __urls.py__ file, and calls the __view__ that matches the URL.
- The __view__, located in __views.py__, checks for relevant models.
- The __models__ are imported from the __models.py__ file.
- The __view__ then sends the data to a specified template in the template folder.
- The template contains HTML and Django tags, and with the data it returns finished HTML content back to the browser.

---

## Steps
- Create Venv
- Install Django, check version [django-admin --version]
- Create Project [django-admin startproject <Project_Name>]
- Crete App [django-admin startapp <App_Name>]. We're gonna write <projects> for our case.
- Run Server [python manage.py runserver] (OPTIONAL)

## Configuration

#### 1. Portfolio/settings.py
```
# Add your app to INSTALLED_APPS:
INSTALLED_APPS = [
    # Default Django apps...
    'projects',  # Add your app here
    # Other apps you might need...
]

# Set up the static files and media files configurations (for CSS, JavaScript, images, etc.):
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Set up templates (if you haven’t already):
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Add this line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

#### 2. URL Configuration
__Project-level URL configuration (Portfolio/urls.py):__
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),  # Include your app's URLs
]
```
__App-level URL configuration (projects/urls.py):__
Create a file urls.py inside your projects app directory and define your app’s URLs:
```
from django.urls import path
from projects import views

urlpatterns = [
    path('', views.index, name='index'),  # Note, we're importing the functions from the views.py
    path('about/', views.about, name='about'),
]
```
__Create a simple view in projects/views.py:__
```
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # Renders the template from 'templates/index.html'

def about(request): 
    return render(request, "about.html")  # Renders the template from 'templates/about.html'
```

#### 3. Database Configuration
If your portfolio requires dynamic content or data storage, use:
```
python manage.py makemigrations
python manage.py migrate
```