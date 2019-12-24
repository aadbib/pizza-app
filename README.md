# Pizza App

## Applications

### Accounts
The account application contains the extended User model and handling the register, login and logout views.

### Home
The Home application contains the non-authenticated views and the css properties.
Furthermore, it contains the base/layout template that all applications inherit from.

### Inventory
The Inventory application contains the static models (without relationships) for rendering
the menu items, and the views neccesary for creating orders. The models define the structure of
the data that is used by the order application for creating orders. 

### Orders
The orders application contains the models for creating orders and order-items, and the
views for viewing and completing the orders.

### Pizza
Pizza contains all necessary project configuraton files for setting up the pizza application.

## Others

### db.sqlite3
This file contains the (in-memory) for storing the web application data.

### manage.py
This file contains the startup script for starting the web application, and takes up additional
parameters for extra functionality. For running the application, execute the following
command:
>   python manage.py runserver

### script.py
This file loads up de database with all inventory-items needed to create the menu, as well as
creating two users, a normal and a admin user used for testing purposes.

### powerscript.ps1
This file contains commands for deleting the migrations, setting up new migrations and
migrating the models, as well as running the script.py file above for initialising the inventory
items.

## Review
Together with a classmate (Yana) we looked at my application and everything was fine...
Until we found out that when removing a topping on a pizza, the topping prices were not
recalculated dynamically and correctly. This is fixed now, prices matter!