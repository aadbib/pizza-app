# Importeer path van urls om de urls te definieren en de views om de urls te mappen aan functies
from django.urls import path
from . import views

# Definieer de urls en de gemapte functies/views
urlpatterns = [
    path("shopping_cart", views.shopping_cart, name="shopping_cart"),
    path("orders", views.orders, name="orders")
]