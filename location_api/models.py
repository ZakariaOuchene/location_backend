from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.conf import settings


class Manager(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    tel = models.CharField(max_length=25, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.password = make_password(self.password)

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email

class Car(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
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
    
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    
class User(models.Model):
    GENDER_CHOICES = (
        ("Femme", "Femme"),
        ("Homme", "Homme"),
    )
    
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birthday = models.DateField()
    tel = models.CharField(max_length=25, blank=True)
    pays = models.CharField(max_length=255, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    license_number = models.CharField(max_length=50)
    cin_passport = models.CharField(max_length=50, blank=True)
    paiement = models.ManyToManyField('Paiement', related_name='users', blank=True)

    def __str__(self):
        return self.email
    
class PickupPoint(models.Model):
    id_pickup = models.AutoField(primary_key=True)
    lieu = models.CharField(max_length=100)
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    
class Booking(models.Model):
    code_booking = models.CharField(max_length=7, unique=True, default="BK01")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_book = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
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

class Tarifs(models.Model):
    id_tarif = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    max_duration = models.IntegerField()
    min_duration = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

class Paiement(models.Model):
    name = models.CharField(max_length=30, blank=True)
    numCard = models.CharField(max_length=20, blank=True)
    expDate = models.CharField(max_length=7, blank=True)
    securityCode = models.PositiveIntegerField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paiements')

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