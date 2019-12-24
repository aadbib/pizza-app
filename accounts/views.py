from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, redirect
from accounts.forms import UserForm, LoginForm
from .models import *

# Maak lege custom Login Forms aan die we telkens gaan gebruiken
form = LoginForm
reg_form = UserForm

def login_view(request):

    # Sla de url op waar de user op geklikt heeft, maar waar hij eerst voor moet authenticeren
    url = request.POST.get('next')

    if request.user.is_authenticated:

            # Redirect wanneer gebruiker al ingelogd is!
            return HttpResponseRedirect(reverse("menu"))

    # Als we met een POST-request te maken hebben...
    if request.method == 'POST':

        # Verkrijg de username en password van de user en authenticeer de gegevens
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Als user geauthenticeerd is
        if user is not None:

            # Log de user in
            login(request, user)

            # Als de user op een route geklikt had waar hij voor moest authenticeren...
            if url !='':

                # Redirect de user naar de url waar hij/zij op geklikt heeft
                return redirect(url)

            # Anders...
            else:

                # Redirect de user naar de menu-view
                return HttpResponseRedirect(reverse("menu"))

        # Anders, render de login page met een fout-melding
        else:
            return render(request, "accounts/login.html", {'form': form, "error": "Invalid credentials."})

    # Bij een GET-request gaan we de view aan de user geven
    else:
        return render(request, "accounts/login.html", {'form': form})

# Log-out route/view
def logout_view(request):

    # Log de user uit
    logout(request)

    # Render de login-view met een succes-melding
    return render(request, "accounts/login.html", {"form":form, "logout": "You have succesfully logged out!"})

# Registreer view/route
def register(request):

    # Als we met een POST-request te maken hebben...
    if request.method == 'POST':

        # Maak een custom_Form aan die we zelf hebben gedefinieerd
        user_form = reg_form(request.POST)

        # is_valid functie om te controlleren of de velden correct zijn ingevuld
        if user_form.is_valid():

            # Controle om te kijken of de user al in de database bestaat, return error als het zo is
            if Account.objects.filter(username=user_form.cleaned_data['username']).exists():
                return render(request, 'accounts/register.html', {
                    'form': user_form,
                    'error_message': 'Username already exists.'
                })

            # Als de user niet in de database bestaat...
            else:

                # Maak user aan d.m.v. Account-class die we zelf gedefinieerd hebben om custom fields te maken
                user = Account.objects.create_user(
                    username=user_form.cleaned_data['username'],
                    password=user_form.cleaned_data['password'],
                    email = user_form.cleaned_data['email'],
                    city = user_form.cleaned_data['city'],
                    first_name = user_form.cleaned_data['first_name'],
                    last_name = user_form.cleaned_data['last_name']
                )

                # Creer user in database
                user.save()

                # Redirect naar de login-route
                return render(request, "accounts/login.html", {"form": form, "success":"You have successfully created an account!"})

    # Als we met een GET-request te maken hebben...
    else:

        # Als de user ingelogd is...
        if request.user.is_authenticated:

            # Log de user uit
            logout(request)

        # En render vervolgens de registreer view
        return render(request, "accounts/register.html", {'form': reg_form})