# URL patterns
from django.urls import path
from projects import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("projects/", views.projects, name="projects"),
    path("projects/machine_learning/", views.machine_learning, name="machine_learning"),
    path("projects/deep_learning/", views.deep_learning, name="deep_learning"),
    path("projects/generative_ai/", views.generative_ai, name="generative_ai"),
    
    path("connect/", views.connect, name="connect"),
]