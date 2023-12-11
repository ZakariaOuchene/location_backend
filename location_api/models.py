from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os
from django.contrib.auth.hashers import make_password

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
    code = models.CharField(max_length=10, unique=True, default="AD01")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = "code"
    
    def save(self, *args, **kwargs):

        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.password = make_password(self.password)

        # Generate the code if it's a new user
        if not self.pk:

            prefix = 'CL' if isinstance(self, Client) else 'AD'

            max_code = User.objects.filter(code__startswith=prefix).order_by(
                '-code').values_list('code', flat=True).first()
            if max_code:
                sequence_number = int(max_code[2:]) + 1
            else:
                sequence_number = 1
            self.code = f"{prefix}{sequence_number:02d}"

        # # image

        # if self.id:

        #     old_instance = User.objects.get(id=self.id)
        #     if self.image != old_instance.image:
        #         if (
        #             old_instance.image
        #         ):
        #             os.remove(old_instance.image.path)
        # if self.is_seller:
        #     # If the user is a seller, ensure that the required seller fields are not blank or null
        #     if not self.rue or not self.pays:
        #         raise ValueError("Seller fields are required for sellers.")

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

    def __str__(self):

        return self.email
    
class Client(User):
    tel = models.CharField(max_length=25, blank=True)
    pays = models.CharField(max_length=255, blank=True)
    birthday = models.DateField()
    license_number = models.CharField(max_length=50)
    cin_passport = models.CharField(max_length=50, blank=True)
    paiement = models.ManyToManyField('Paiement', related_name='client', blank=True)
    
    def __str__(self):
        return self.email

class Car(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='car_images/')
    matricule = models.CharField(max_length=50)
    passenger_number = models.IntegerField()
    air_conditioning = models.BooleanField(default=False)
    disponibilte = models.BooleanField(default=True)
    FUEL_CHOICES = (
        ("ESSENCE", "ESSENCE"),
        ("DIESEL", "DIESEL"),
    )
    fuel = models.TextField(max_length=50, choices=FUEL_CHOICES)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model}"
    
class Tarifs(models.Model):
    id_tarif = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    max_duration = models.IntegerField()
    min_duration = models.IntegerField()
    price_per_day = models.IntegerField()
    
class PickupPoint(models.Model):
    id_pickup = models.AutoField(primary_key=True)
    lieu = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    
class Assurance(models.Model):
    nom = models.CharField(max_length=255)
    prix_par_jour = models.IntegerField()
    
class ChildChair(models.Model):
    age = models.IntegerField()
    prix_jrs = models.IntegerField()
    diponible = models.BooleanField(default=True)
    
class Booking(models.Model):
    code_booking = models.CharField(max_length=7, unique=True, default="BK01")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assurance = models.ForeignKey(Assurance, on_delete=models.CASCADE, null=True, blank=True)
    childchair = models.ForeignKey(ChildChair, on_delete=models.CASCADE, null=True, blank=True)
    date_book = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    nbr_jrs = models.IntegerField()
    pickup_start = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='bookings_pickup_start')
    pickup_end = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name='bookings_pickup_end')
    payement = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
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
        return f"{self.user.email} - {self.car} - {self.start_date} to {self.end_date}"

class Paiement(models.Model):
    name = models.CharField(max_length=30, blank=True)
    numCard = models.CharField(max_length=20, blank=True)
    expDate = models.CharField(max_length=7, blank=True)
    securityCode = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return self.name

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
