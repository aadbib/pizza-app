# Importeer de library en models om de models aan de admin site te kunnen registreren
from django.contrib import admin
from .models import *

# Registreer model voor admin_site
admin.site.register(Account)