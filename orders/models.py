# Importeer de nodige models om de relaties met order-items vast te kunnen leggen en de huidige datum te bepalen
from accounts.models import *
from inventory.models import *
from datetime import datetime

                                        # --- USER-ORDER-SYSTEM -- #
# Order-model
class Order(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="order_users")
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(default=datetime.now())

    # Functie voor het verkrijgen van alle order items van een order
    def show_order(self):
        pizzas = Pizza_Order.objects.filter(order_id=self.id)
        pastas = Pasta_Order.objects.filter(order_id=self.id)
        salads = Salad_Order.objects.filter(order_id=self.id)
        dinner_platters = Dinner_Platters_Order.objects.filter(order_id=self.id)
        subs = Sub_Order.objects.filter(order_id=self.id)
        toppings = Topping_Order.objects.filter(order_id=self.id)

        all = []

        for food_order in pizzas, pastas, salads, dinner_platters, subs, toppings:
            for food in food_order:
                all.append(food)

        return all

    # Functie voor het verwijderen van alle order items van een order
    def delete_order(self):
        order = self.show_order()

        for food in order:
            food.delete()

    # Getter-functie voor het afronden van een order
    def get_ordered(self):
        return self.ordered

    # Setter-functie voor het afronden van een order
    def set_ordered(self):
        self.ordered = True
        self.save()

    # Functie voor het maken van het totale prijs, als property zodat django-template erbij kan
    @property
    def order_price(self):

        # Base totale prijs
        total_price = 0.00

        # Verkrijg alle food-items in order
        orders = self.show_order()

        # Loop door deze food-items heen
        for food in orders:

            # Pak de gegeven vaste prijzen van de food-items, waarbij toppings wordt overgeslagen
            if not isinstance(food, Topping_Order):
                total_price += float(food.name.price)

            # Als we met een Topping te maken hebben
            else:
                # Als er een topping_prijs is bepaald (dus geen None)
                if food.price:

                    # Cast de toppingsprice naar float, omdat het op twee decimalen geformat is
                    toppings_price = float(food.price)

                    # Tel dit met de totale prijs op
                    total_price += toppings_price

        # Formateer het bedrag in een getal met twee decimalen
        total_price = f'{total_price: .2f}'

        # Return de totale price :)
        return total_price

# Pizza-Order-model
class Pizza_Order(models.Model):
    name = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="pizza_names")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    # Functie voor het toevoegen van een topping
    def add_topping(self, Topping):
        Topping.pizza_type = self
        Topping.save()

    # Functie voor het verwijderen van een topping
    def del_topping(self, Topping):

        # Verwijder de topping
        Topping.delete()

        # Controleer hoeveel toppings er nog op de pizza zitten
        counter = self.get_toppings_count()

        # Pak alle toppings die op de pizza zitten
        toppings = Topping_Order.objects.filter(pizza_type=self)

        # We gaan de toppings-prijzen re-assignen
        for top in range(0, counter):
            toppings[top].update_price(top + 1)

    #  Get-functie voor het verkrijgen van aantal toppings
    def get_toppings_count(self):
        topping_count = self.pizza_topping.count()

        return topping_count

    def __str__(self):
        return f"{self.name}"

# Dinner-Platters-Order-model
class Dinner_Platters_Order(models.Model):
    name = models.ForeignKey(Dinner_Platter, on_delete=models.CASCADE, related_name="dinner_platter_names")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

# Subs-Order-model
class Sub_Order(models.Model):
    name = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="sub_names")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    # Functie voor het toevoegen van een topping
    def add_topping(self, Topping):
        Topping.sub_type = self
        Topping.save()

    # Functie voor het verwijderen van een topping
    def del_topping(self, Topping):
        Topping.delete()

    #  Get-functie voor het verkrijgen van aantal toppings
    def get_toppings_count(self):
        topping_count = self.sub_topping.count()

        return topping_count

    def __str__(self):
        return f"{self.name}"

# Topping-order-model, 1 op veel relatie met pizza en subs
class Topping_Order(models.Model):
    name = models.ForeignKey(Topping, on_delete=models.CASCADE, related_name="topping_names")
    pizza_type = models.ForeignKey(Pizza_Order, on_delete=models.CASCADE, related_name="pizza_topping", blank=True, null=True)
    sub_type = models.ForeignKey(Sub_Order, on_delete=models.CASCADE, related_name="sub_topping", blank=True, null=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    # Async bijhouden wat de prijs is van een topping op een gegeven moment in tijd
    price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=8)

    # Functie die als property gaat dienen om de prijs telkens te bepalen
    def toppings_price(self, delete=False, index=None):

        # Als het een toppings op een pizza is
        if self.pizza_type is not None:

            # Pak dan de nodige attributen om de toppings-price van deze pizza te bepalen
            toppings = self.pizza_type.get_toppings_count()
            pizza_type = self.pizza_type.name.get_pizza_type()
            pizza_size = self.pizza_type.name.get_size()

            # Een price-dictionary om de prijzen te mappen aan de pizzas
            price_list = {
                "Regular": {
                    "Small": {1: 1.00, 2: 1.50, 3: 1.00, 4: 1.55},
                    "Large": {1: 2.00, 2: 2.00, 3: 2.00, 4: 2.00}
                },
                "Silician": {
                    "Small": {1: 2.00, 2: 2.00, 3: 1.00, 4: 1.00},
                    "Large": {1: 2.00, 2: 2.00, 3: 2.00, 4: 1.00}
                }
            }

            if delete:
                topping_price = price_list[pizza_type][pizza_size][index]

            else:
                # Bepaal de toppings_price van de pizza
                topping_price = price_list[pizza_type][pizza_size][toppings + 1]

        # Als de topping op een sub is geplaatst, bepaal dan een andere prijs
        elif self.sub_type is not None:
            topping_price = 0.50

        # Als de topping nergens op geplaatst is
        else:
            # Zet dan de toppings_price op null
            topping_price = None

        # Return de topping prijs
        return topping_price

    def __str__(self):
        return f"{self.name} - {self.pizza_type.name.get_slug()}" if self.pizza_type is not None else f"{self.name} - {self.sub_type.name.get_slug()}"

    """"Save method toegevoegd omdat op het moment van aanroepen van method toppings_price in Order, dan wordt alleen de laatste value gepakt.
        Door dit op te slaan als een echte property, wordt in de tijd vastgesteld hoeveel de topping kost (async)
        Dit nog extra verbeterd door de toppingsprijs in de view aan te passen wanneer er een delete plaatsvindt"""
    def save(self, delete=False, index=None, *args, **kwargs):
        if not delete:
            self.price = self.toppings_price()
        else:
            self.price = self.toppings_price(True, index)

        super(Topping_Order, self).save(*args, **kwargs)

    # Set price functie om in de view bij het verwijderen van shopping cart een recalculatie uit te voeren
    def update_price(self, index):
        self.save(True, index)

# Pasta-Order-model
class Pasta_Order(models.Model):
    name = models.ForeignKey(Pasta, on_delete=models.CASCADE, related_name="pasta_names")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

# Salad-Order-model
class Salad_Order(models.Model):
    name = models.ForeignKey(Salad, on_delete=models.CASCADE, related_name="salad_names")
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"