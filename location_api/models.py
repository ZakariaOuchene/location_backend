from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, code, password=None):
        user = self.create_user(code, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ("Femme", "Femme"),
        ("Homme", "Homme"),
    )
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=30, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, default="AD01")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True)
    ville = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=25, blank=True)
    image = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )
    
    objects = UserManager()

    USERNAME_FIELD = "code"
    
    def save(self, *args, **kwargs):

        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.password = make_password(self.password)

        # Generate the code if it's a new user
        if not self.pk:

            prefix = 'AD'

            max_code = User.objects.filter(code__startswith=prefix).order_by(
                '-code').values_list('code', flat=True).first()
            if max_code:
                sequence_number = int(max_code[2:]) + 1
            else:
                sequence_number = 1
            self.code = f"{prefix}{sequence_number:02d}"

        # # image
        if self.id:

            old_instance = User.objects.get(id=self.id)
            if self.image != old_instance.image:
                if (
                    old_instance.image
                ):
                    os.remove(old_instance.image.path)

        if self.first_name and self.last_name:
            self.username = f"{self.first_name}_{self.last_name}"

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
    
class Manager(User):
    ROLE_CHOICES = (
        ("SUPERADMIN", "SUPERADMIN"),
        ("ADMIN", "ADMIN"),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="ADMIN")
    etat = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='car_images/')
    matricule = models.CharField(max_length=50)
    passenger_number = models.IntegerField()
    air_conditioning = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)
    GREARBOX_CHOICES = (
        ("MANUELLE", "MANUELLE"),
        ("AUTOMATIQUE", "AUTOMATIQUE"),
    )
    gearBox =  models.TextField(max_length=50, choices=GREARBOX_CHOICES)
    FUEL_CHOICES = (
        ("ESSENCE", "ESSENCE"),
        ("DIESEL", "DIESEL"),
    )
    fuel = models.TextField(max_length=50, choices=FUEL_CHOICES)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"
    
    def get_brand_and_model(self):
        return f"{self.brand} {self.model}"
    
class Tarifs(models.Model):
    id_tarif = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    price_more_month = models.IntegerField()
    price_week= models.IntegerField()
    price_tree_days = models.IntegerField()
    price_two_week = models.IntegerField()
    price_more_two_week = models.IntegerField()
    
class PickupPoint(models.Model):
    id_pickup = models.AutoField(primary_key=True)
    lieu = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    
class Booking(models.Model):
    code = models.CharField(max_length=7, unique=True, default="BK01")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    assurance = models.BooleanField(default=False)
    childchair = models.IntegerField(default=0)
    rehausseur = models.IntegerField(default=0)
    conducteur = models.BooleanField(default=False)
    date_book = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    nbr_jrs = models.IntegerField()
    pickup_start = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='bookings_pickup_start')
    pickup_end = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='bookings_pickup_end')
    archive = models.BooleanField(default=False)
    repayment = models.BooleanField(default=False)
    payement = models.BooleanField(default=False)
    surPlace = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price_HT = models.DecimalField(max_digits=10, decimal_places=2)
    tel = models.CharField(max_length=25, blank=True)
    email = models.EmailField(max_length=255, blank=True,)
    pays = models.CharField(max_length=50, blank=True)
    codePostal = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField()
    cin_passport = models.CharField(max_length=50, blank=True)
    GENDER_CHOICES = (
        ("Femme", "Femme"),
        ("Homme", "Homme"),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    def save(self, *args, **kwargs):
        # Generate the code if it's a new complaint
        if not self.pk:
            prefix = 'Bk'

            max_code = Booking.objects.filter(code__startswith=prefix).order_by(
                '-code').values_list('code', flat=True).first()
            if max_code:
                sequence_number = int(max_code[2:]) + 1
            else:
                sequence_number = 1

            self.code = f"{prefix}{sequence_number:02d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cin_passport} - {self.car} - {self.start_date} to {self.end_date}"

class Review(models.Model):
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    comment = models.TextField()
    date_review = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.date}"
