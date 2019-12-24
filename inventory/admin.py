# Importeer de library en models om de models aan de admin site te kunnen registreren
from django.contrib import admin
from .models import *

# Registreer models voor admin_site
admin.site.register(Pizza)
admin.site.register(Sub)
admin.site.register(Topping)
admin.site.register(Pasta)
admin.site.register(Dinner_Platter)
admin.site.register(Salad)