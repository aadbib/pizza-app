# Importeer de nodige libraries om models te maken en om de User-model te extenden en managers te maken
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

                                # ---- User_extension ---- #

# Class dat gebruikt wordt om users en super-users te creeren, is de manager van class Account
class MyAccountManager(BaseUserManager):

    # Functie om een user te creeren
    def create_user(self, username, email, city, first_name, last_name, password=None):

        # Kleine error-handling
        if not username:
            raise ValueError("Users must have an username")

        if not email:
            raise ValueError("Users must have an email address")

        # Creer de user
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            city=self.normalize_email(city),
            first_name=self.normalize_email(first_name),
            last_name=self.normalize_email(last_name)
        )

        # Zet het wachtwoord
        user.set_password(password)

        # Sla de user op
        user.save(using=self._db)

        # Return de user
        return user

    # Functie om superuser te creeren, roept create_user functie aan
    def create_superuser(self, username, password, email):
        user = self.create_user(
            username=username,
            password=password,
            email=self.normalize_email(email),
            city="Amsterdam",
            first_name="",
            last_name=""
        )

        # Zet de attributen die een super_user definieren op True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

# Class die de User-model definieert, uit deze class wordt een user-object aangemaakt
class Account(AbstractBaseUser):

    # Properties die een user potentieel kan hebben
    username = models.CharField(verbose_name="username", max_length=30, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60)
    city = models.CharField(verbose_name="city", max_length=80)
    first_name = models.CharField(verbose_name="first_name", max_length=30)
    last_name = models.CharField(verbose_name="last_name", max_length=6)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Zet de verplichte velden en het veld dat weergegeven wordt voor een user
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    # Maak een accountmanager aan door de constructor aan te roepen
    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # Getter-functie om te kijgen of een user admin is
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Getter functie om de module permissies van een user op te vragen
    def has_module_perms(self, app_label):
        return True