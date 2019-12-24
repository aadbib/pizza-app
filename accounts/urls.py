# Importeer path van urls om de urls te definieren en de views in de applicatie om aan route te kunnen mappen
from django.urls import path
from . import views

# Definieer de urls en de gemapte functies/views
urlpatterns = [
    path("login_view", views.login_view, name="login_view"),
    path("register", views.register, name="register"),
    path("logout_view", views.logout_view, name="logout_view")
]