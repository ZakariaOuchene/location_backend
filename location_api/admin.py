from django.contrib import admin

from .models import User, Manager, Car, CarImage, PickupPoint, Booking, Tarifs, Paiement, Payment

admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Car)
admin.site.register(Manager)
admin.site.register(CarImage)
admin.site.register(PickupPoint)
admin.site.register(Booking)
admin.site.register(Tarifs)
admin.site.register(Paiement)
admin.site.register(Payment)

