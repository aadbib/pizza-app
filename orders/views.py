#Importeer de nodige libraries
from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import email.mime.application

# Functie om de alle food-items in een order van een user te krijgen
def get_orders(user_id, key):

    # Lege order_dict
    order_dict = {}

    # Try/Except om de juiste orders te zoeken en als er niks gevonden is, lege list
    try:

        # We gaan de key afhandelen om te bepalen welke gegevens van de order opgehaald moeten worden


        # Als de key 'latest' is, pak dan de laatste order die succesvol georderd is
        if key == "latest":

            orders = Order.objects.filter(user_id=user_id, ordered=True).latest('id')

            order_dict[orders] = orders.show_order()

            return order_dict

        # Als de key unfinished is, pak dan de order die nog niet georderd is
        elif key == "unfinished":
            orders = Order.objects.filter(user_id=user_id, ordered=False)

        # Anders
        else:

            # Pak alle succevolle orders die georderd zijn als de user een admin is
            if user_id.is_admin == True:
                orders = Order.objects.filter(ordered=True)

            # Anders, pak alleen de succesvolle orders die door de user zelf georderd is
            else:
                orders = Order.objects.filter(user_id=user_id, ordered=True)

    # Als er iets fout gegaan is, initialiseer een lege list
    except:
        orders = []

    # Vul de orders dict
    for order in orders:
        order_dict[order] = order.show_order()

    # Return de order_dict
    return order_dict

# Mail functie om na het successvol afronden van een order een mail te sturen
def mail_orders(user, filename, name):

    # Zet de (encrypted) verbinding naar de SMTP server van Google op
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('pythontesting555@gmail.com', 'Utrecht007')

    # MIME-object wordt aangemaakt, en de bericht-headers worden opgezet
    msg = MIMEMultipart()
    msg['Subject'] = 'Your order is successful'
    msg['From'] = 'Piatto Italiano'
    msg['To'] = user.email
    txt = MIMEText(f'Order: {name} has successfully been completed.\nYou can view your orde-status at: http://127.0.0.1:8000/orders')
    msg.attach(txt)

    # Bestand wordt als 'attachment' aan de email toegevoegd
    filename = filename
    fo = open(filename, 'rb')
    file = email.mime.application.MIMEApplication(fo.read(), _subtype=".html")
    fo.close()
    file.add_header('Content-Disposition', 'attachment', filename=name)
    msg.attach(file)

    # Verzend de email en sluit de verbinding
    mail.send_message(msg)
    mail.quit()


@login_required()
def shopping_cart(request):

    # Zet de message-value als initialisatie op null
    message = None

    # Verkrijg order die nog niet gedaan is
    order_dict = get_orders(request.user, "unfinished")

    # Als de user op een knop in shoppingcart gedrukt heeft
    if request.method == "POST":

        # Als de user op de 'complete' knop gedrukt heeft
        if 'complete' in request.POST:

            # Verkrijg de order_id van de order die nog niet afgerond is
            order_id = Order.objects.get(user_id=request.user, ordered=False).id

            # Zet deze order op 'ordered'
            Order.objects.get(user_id=request.user, ordered=False).set_ordered()

            # Creer een bijbehorende bericht
            message = "Your have completed your order!"

            # Verkrijg laatste order
            order_dict = get_orders(request.user, "latest")

            # Render template met alle items naar een string
            content = render_to_string('orders/shopping_cart.html', {"order": order_dict, "message": message})

            # Creer een file-naam variabele
            name = f'order-{order_id}'

            # Pak het pad waar we de orders gaan opslaan
            file = f'orders/static/orders/{name}.html'

            # Kopieer dit naar een externe html bestand
            with open(file, 'w') as static_file:
                static_file.write(content)

            # Mail deze html bestand naar user
            mail_orders(request.user, file, name)

        # Als de user op de delete knop gedrukt heeft
        elif 'delete' in request.POST:

            # Verwijder de order die nog niet 'ordered' is
            Order.objects.get(user_id=request.user, ordered=False).delete_order()

            # Creer een bijbehorende bericht
            message = "Your order has been deleted!"

            # Refresh de huidige order_dict om te renderen
            order_dict = get_orders(request.user, "unfinished")

        # Als de user een speciefieke item wilt verwijderen
        else:

            # Maak een dictionary die alle soorten eten mapt met de nodige functies om de juiste informatie op te halen
            food_dict = {
                "Topping": [Topping_Order.objects.get, Topping_Order.objects.filter],
                "Pizza": Pizza_Order.objects.get,
                "Sub": Sub_Order.objects.get,
                "Pasta": Pasta_Order.objects.get,
                "Salad": Salad_Order.objects.get,
                "Platter": Dinner_Platters_Order.objects.get
            }

            # Split de request in food_type en id
            food_item = request.POST["food_item"].split('/')

            # Pak de juiste attributen van de list
            food_type = food_item[0]
            food_id = food_item[1]

            # Query de juiste order_id om de food_item van de juiste order te verwijderen
            order_id = Order.objects.get(user_id=request.user, ordered=False).id

            # Als we een topping gaan verwijderen
            if food_type == "Topping":

                # Pak de topping_item
                top_item = food_dict[food_type][0](id=food_id, order_id=order_id)

                # Als het een topping op een pizza is
                if top_item.pizza_type is not None:

                    # Pak de pizza en nodige attriubuten van de pizza om de values te reassignen
                    pizza = top_item.pizza_type

                    # Verwijder de topping_item
                    top_item.delete()

                    # Calculeer de pizza toppings
                    counter = pizza.get_toppings_count()

                    # Pak alle toppings die in de order zitten
                    toppings = food_dict[food_type][1](order_id=order_id, pizza_type=pizza)

                    # We gaan de toppings-prijzen re-assignen
                    for top in range(0, counter):
                        toppings[top].update_price(top + 1)

                # Als het een topping op een Sub is, dan gewoon verwijderen
                else:
                    food_dict[food_type][0](id=food_id, order_id=order_id).delete()
            else:
                # Gebruik de dictionary om de juiste functie aan te roepen voor het juiste object, en verwijder het object
                food_dict[food_type](id=food_id, order_id=order_id).delete()

            # Refresh de huidige order_dict om te renderen
            order_dict = get_orders(request.user, "unfinished")

    return render(request, "orders/shopping_cart.html", {"order":order_dict, "message":message})

# Order route-view, waar we users hun bestelde orders kunnen laten zien
@login_required()
def orders(request):

    # Verkrijg alle gelukte orders, admins krijgen ook die van de users
    order_dict = get_orders(request.user, "finished")

    # Controleer of de user een admin is om zo in de template te bepalen of de usernames gerenderd moeten worden
    is_admin = request.user.is_admin

    # Return de view
    return render(request, "orders/orders.html", {"order": order_dict, "is_admin":is_admin})