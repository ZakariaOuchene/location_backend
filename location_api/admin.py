from django.contrib import admin

from .models import User, Manager, Car, PickupPoint, Booking, Tarifs, Review

admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Car)
admin.site.register(PickupPoint)
admin.site.register(Booking)
admin.site.register(Tarifs)
admin.site.register(Review)


