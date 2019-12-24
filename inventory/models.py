# Importeer de ndoige library om modellen te maken en om slugs te maken voor modellen (voor de url)
from django.db import models
from django.utils.text import slugify

#   --- Inventory Models ---    #

# Pizza-model
class Pizza(models.Model):
    food_type = models.CharField(max_length=15, default="Pizza")
    pizza_type = models.CharField(max_length=15)
    size = models.CharField(max_length=6)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField()

    # Django doesn't support composite-keys, workaround!
    class Meta:
        unique_together = (("pizza_type", "size"),)

    def get_pizza_type(self):
        return self.pizza_type

    def get_size(self):
        return self.size

    def get_price(self):
        return self.price

    def get_slug(self):
        return self.slug

    # Override save-functie om dynamische slug toe te voegen voor gebruik in URL
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.food_type}-{self.pizza_type}")
        super(Pizza, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_type} - {self.pizza_type} - {self.size}"

# Sub-model
class Sub(models.Model):
    food_type = models.CharField(max_length=15, default="Sub")
    sub_type = models.CharField(max_length=32)
    size = models.CharField(max_length=6)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField()

    # Django doesn't support composite-keys, workaround!
    class Meta:
        unique_together = (("sub_type", "size"),)

    def get_sub_type(self):
        return self.sub_type

    def get_size(self):
        return self.size

    def get_price(self):
        return self.price

    def get_slug(self):
        return self.slug

    # Override save-functie om dynamische slug toe te voegen voor gebruik in URL
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.food_type}-{self.sub_type}")
        super(Sub, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_type} - {self.sub_type} - {self.size}"

# Topping-model
class Topping(models.Model):
    food_type = models.CharField(max_length=15, default="Topping")
    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return f"{self.food_type} - {self.name}"

# Pasta-model
class Pasta(models.Model):
    food_type = models.CharField(max_length=15, default="Pasta")
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(unique=True)

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_slug(self):
        return self.slug

    # Override save-functie om dynamische slug toe te voegen voor gebruik in URL
    def save(self, *args, **kwargs):
        self.slug = self.slug = slugify(f"{self.food_type}-{self.name}")
        super(Pasta, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_type} - {self.name}"

# Salads-model
class Salad(models.Model):
    food_type = models.CharField(max_length=15, default="Salad")
    name = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(unique=True)

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_slug(self):
        return self.slug

    # Override save-functie om dynamische slug toe te voegen voor gebruik in URL
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.food_type}-{self.name}")
        super(Salad, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_type} - {self.name}"

# Dinner-platters-model
class Dinner_Platter(models.Model):
    food_type = models.CharField(max_length=15, default="Platter")
    dinner_platters_type = models.CharField(max_length=24)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size = models.CharField(max_length=6)
    slug = models.SlugField()

    # Django doesn't support composite-keys, workaround!
    class Meta:
        unique_together = (("dinner_platters_type", "size"),)

    def get_dinner_platters_type(self):
        return self.dinner_platters_type

    def get_size(self):
        return self.size

    def get_price(self):
        return self.price

    def get_slug(self):
        return self.slug

    # Override save-functie om dynamische slug toe te voegen voor gebruik in URL
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.food_type}-{self.dinner_platters_type}")
        super(Dinner_Platter, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.food_type} - {self.dinner_platters_type} - {self.size}"