# Importeer path van urls om de urls te definieren en de views om de urls te mappen aan functies
from django.urls import path
from . import views

# Definieer de urls en de gemapte functies/views
urlpatterns = [
    path("menu", views.menu, name="menu"),
    path("menu_food/<food_slug>", views.menu_food, name="menu_food")
]