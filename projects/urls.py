from django.urls import path
from projects import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("projects/", views.projects, name="projects"),
    path("contact/", views.contact, name="contact"),
]