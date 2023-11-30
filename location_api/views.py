from django.shortcuts import render
from rest_framework import permissions, viewsets

from .models import User, Manager, Car, CarImage, PickupPoint, Booking, Tarifs, Paiement, Payment
from .serializers import UserSer, ManagerSer, CarSer, CarImageSer, PickupPointSer, BookingSer, TarifsSer, PaiementSer, PaymentSer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSer
    
class ManagerView(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSer
    
class CarView(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSer
    
class CarImageView(viewsets.ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSer
    
class PickupPointView(viewsets.ModelViewSet):
    queryset = PickupPoint.objects.all()
    serializer_class = PickupPointSer
    
class PickupPointView(viewsets.ModelViewSet):
    queryset = PickupPoint.objects.all()
    serializer_class = PickupPointSer
    
class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSer
    
class TarifsView(viewsets.ModelViewSet):
    queryset = Tarifs.objects.all()
    serializer_class = TarifsSer
    
class PaiementView(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSer
    
class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSer