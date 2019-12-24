# Importeer de nodige library om de views te renderen
from django.shortcuts import render

# Simpele index/home view
def index(request):
    return render(request, "home/index.html")

# Simpele contact view
def contact(request):
    return render(request, "home/contact.html")