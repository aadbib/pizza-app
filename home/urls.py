# Importeer path van urls om de urls te definieren en de views om de urls te mappen aan functies
from django.urls import path
from . import views

# Definieer de urls en de gemapte functies/views
urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact")
]