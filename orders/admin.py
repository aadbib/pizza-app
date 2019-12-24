# Importeer de library en models om de models aan de admin site te kunnen registreren
from django.contrib import admin
from .models import *

# Registreer models voor admin_site
admin.site.register(Pizza_Order)
admin.site.register(Topping_Order)
admin.site.register(Sub_Order)
admin.site.register(Pasta_Order)
admin.site.register(Dinner_Platters_Order)
admin.site.register(Salad_Order)
admin.site.register(Order)