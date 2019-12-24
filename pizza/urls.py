"""pizza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.pizza, name='pizza')
Class-based views
    1. Add an import:  from other_app.views import pizza
    2. Add a URL to urlpatterns:  path('', pizza.as_view(), name='pizza')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Importeer path, include van urls om de urls (van andere apps) te definieren en admin om de admin-site te definieren
from django.contrib import admin
from django.urls import include, path

# Definieer de urls en de gemapte functies/views
urlpatterns = [
    path("", include("accounts.urls")),
    path("", include("home.urls")),
    path("", include("inventory.urls")),
    path("", include("orders.urls")),
    path("admin/", admin.site.urls)
]
