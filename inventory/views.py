# Importeer de nodige libraries voor de views
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from orders.models import *
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required

# Als user is ingelogd, dan is menu toegestaan
@login_required()
def menu(request):

    # Query alle nodige inventory-items om deze in het menu te zetten
    pizza_types = Pizza.objects.values('pizza_type', 'slug').distinct()
    pizza_prices = Pizza.objects.values('pizza_type', 'price')
    toppings = Topping.objects.all()
    sub_types = Sub.objects.values('sub_type', 'slug').distinct()
    sub_prices = Sub.objects.values('sub_type', 'price')
    pastas = Pasta.objects.all()
    salads = Salad.objects.all()
    dinner_types = Dinner_Platter.objects.values('dinner_platters_type', 'slug').distinct()
    dinner_prices = Dinner_Platter.objects.values('dinner_platters_type', 'price')

    return render(request, "inventory/menu.html", {"pizza_types":pizza_types, "pizza_prices":pizza_prices, "toppings":toppings, "sub_types":sub_types, "sub_prices":sub_prices, "pastas":pastas,
                                                "salads":salads, "dinner_types":dinner_types, "dinner_prices":dinner_prices})

# Menu_food route-view
@login_required()
def menu_food(request, food_slug):

    # Alleen wanneer de form ingevuld is, en dus geen get-request is
    if request.method == "POST":

        # Maak een dictionary die alle soorten eten mapt met de nodige functies om de juiste informatie op te halen
        food_dict = {

            "topping": {
                "food": Topping.objects.get,
                "topping_order": Topping_Order
            },
            "Pizza": {
                "food": Pizza.objects.get,
                "food_order": Pizza_Order,
                "food_order_get": Pizza_Order.objects.get
            },
            "Sub": {
                "food": Sub.objects.get,
                "food_order": Sub_Order,
                "food_order_get": Sub_Order.objects.get
            },
            "Pasta": {
                "food": Pasta.objects.get,
                "food_order": Pasta_Order
            },
            "Salad": {
                "food": Salad.objects.get,
                "food_order": Salad_Order
            },
            "Platter": {
                "food": Dinner_Platter.objects.get,
                "food_order": Dinner_Platters_Order
            }
        }

        # Pak de id en colom-naam uit de post
        food = request.POST["food"].capitalize().split('/')

        # Check of de user al een order heeft of niet, zo ja geen nieuwe order
        u, created = Order.objects.get_or_create(user_id=request.user, ordered=False)

        # 2 If-statements, eentje voor het toevoegen van toppings, andere voor het aanmaken van pizza/sub order objects
        if food_slug == "food":

            food_type = food[0]
            food_id = food[1]

            # Query de food_type_object die gekozen is
            food_object = food_dict[food_type]["food"](id=food_id)

            # Maak het food_order_object aan
            food_order_object = food_dict[food_type]["food_order"](name=food_object, order_id=u)

            # Sla het order_object op in de database
            food_order_object.save()

            # Als het een pizza of sub is, ga naar toppings-url
            if food_type in ["Pizza", "Sub"]:

                # Als het een pizza is
                if food_type == "Pizza":

                    # Query alle toppings
                    toppings = Topping.objects.all()

                # Anders... (dus sub)
                else:

                    # Query alleen Mushrooms, Green Peppers en Onions voor de view
                    toppings = Topping.objects.all().filter(name__in = ("Mushrooms", "Green Peppers", "Onions"))

                # Pak de id van de food_order_object om met template mee te sturen
                food_order_id = getattr(food_order_object, "id")

                return render(request, "inventory/toppings.html", {"toppings": toppings, "food": food, "food_order_id": food_order_id})

            # Anders, pak de quantity, maak de food-objects aan en redirect naar shopping cart!
            else:
                try:
                    quantity = int(request.POST["quantity"]) - 1

                except:
                    quantity = 0

                for food in range(0, quantity):

                    # Maak het food_order_object aan
                    food_order_object = food_dict[food_type]["food_order"](name=food_object, order_id=u)

                    # Sla het order_object op in de database
                    food_order_object.save()

                return HttpResponseRedirect(reverse("shopping_cart"))

        # Als we toppings moeten toevoegen of verwijderen voor pizza en subs
        else:

            # Error initiele waarde is none
            error = None

            # Pak de nodige attributen van de template
            topping_name = food[1].title()
            food_type = food[2].capitalize()
            food_order_id = food_slug

            if food_type == "Pizza":

                # Haal alle toppings vanuit de database op
                toppings = Topping.objects.all()

            else:
                toppings = Topping.objects.all().filter(name__in=("Mushrooms", "Green Peppers", "Onions"))

            # Query de topping_type_object die gekozen is
            topping_object = food_dict["topping"]["food"](name=topping_name)

            # Haal de betreffende food_order op waar we de topping aan gaan toevoegen
            food_order_object = food_dict[food_type]["food_order_get"](id=food_order_id, order_id=u)

            # Verkrijg de toppings-count van de pizza en sub
            toppings_count = food_order_object.get_toppings_count()

            # Als we toppings moeten verwijderen
            if 'top_del' in request.POST:

                topping_del = request.POST["top_del"]

                topping_object = Topping_Order.objects.get(id=topping_del)

                food_order_object.del_topping(topping_object)

            # Als we toppings moeten toevoegen
            else:

                # Als de food-object minder dan 4 toppings heeft, en het is een pizza, dan kan er een topping toegevoegd worden
                if toppings_count < 4 and food_type == "Pizza":

                    # Maak het bijbehorende topping_order object aan als de pizza
                    topping_order_object = food_dict["topping"]["topping_order"](name=topping_object, order_id=u)

                    # Sla het topping_object in de database op
                    topping_order_object.save()

                    # Roep functie aan om de topping aan de pizza/sub object toe te voegen
                    food_order_object.add_topping(topping_order_object)

                # Als het geen pizza is, en dus een sub, dan maximaal 3 toppings
                elif toppings_count < 3:

                    # Maak het bijbehorende topping_order object aan als de pizza
                    topping_order_object = food_dict["topping"]["topping_order"](name=topping_object, order_id=u)

                    # Sla het topping_object in de database op
                    topping_order_object.save()

                    # Roep functie aan om de topping aan de pizza/sub object toe te voegen
                    food_order_object.add_topping(topping_order_object)

                else:

                    # Geef error een foutwaarde
                    error = f"Error: Maximum toppingcount of {toppings_count} reached!"

            # Reassign values voor volgende topping
            food = [food_type, food[0], food[1], food_order_id]

            if food_type == "Pizza":

                # Query alle toppings die op de pizza zitten
                all_toppings = food_dict[food_type]["food_order_get"](id=food_order_id, order_id=u).pizza_topping.all()

            else:

                # Query alle toppings die op de sub zitten
                all_toppings = food_dict[food_type]["food_order_get"](id=food_order_id, order_id=u).sub_topping.all()

            return render(request, "inventory/toppings.html", {"toppings": toppings, "food": food, "food_order_id":food_order_id, "all_toppings":all_toppings, "error":error})

    # Anders, gaan we de view regelen
    else:

        # Parse de foodtype en slug uit de url_slug
        food_type = food_slug.split('-')[0]

        # Dictionary om bij de juiste slug de juiste tabel in de database op te zoeken door functies als waardes van keys te assignen, en om de img-url tags in de template aan te passen
        db_lookup = {
            "pizza": [Pizza.objects.filter, "inventory/pizza-img.jpg"],
            "sub": [Sub.objects.filter, "inventory/steak.jpg"],
            "pasta": [Pasta.objects.get, "inventory/pasta.jpg"],
            "salad": [Salad.objects.get, "inventory/salad.jpg"],
            "platter": [Dinner_Platter.objects.filter, "inventory/dinner-plate.png"]
        }

        # Gebruik de juiste db_lookup op basis van de dictionary en zoek op basis van de slug
        foods = db_lookup[food_type][0](slug=food_slug)

        # Pak de juiste pad voor de image voor de type food
        food_img = db_lookup[food_type][1]

        # Check om te kijken of het meerdere objecten zijn die terugkomen of maar een enkele
        if not isinstance(foods, QuerySet):
            foods = [db_lookup[food_type][0](slug=food_slug)]

        return render(request, "inventory/food.html", {"foods":foods, "food_type":food_type, "food_slug":food_slug, "food_img":food_img})