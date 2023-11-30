from rest_framework import serializers

from .models import User, Manager, Car, CarImage, PickupPoint, Booking, Tarifs, Paiement, Payment

class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ManagerSer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = "__all__"
        
class CarImageSer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = "__all__"

class CarSer(serializers.ModelSerializer):
    images = CarImageSer(many=True, read_only=True)
    class Meta:
        model = Car
        fields = "__all__"

class PickupPointSer(serializers.ModelSerializer):
    class Meta:
        model = PickupPoint
        fields = "__all__"

class BookingSer(serializers.ModelSerializer):
    name_pickup_start = serializers.IntegerField(source='PickupPoint.lieu', read_only=True)
    name_pickup_start = serializers.IntegerField(source='PickupPoint.lieu', read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"

class TarifsSer(serializers.ModelSerializer):
    class Meta:
        model = Tarifs
        fields = "__all__"
        
class PaiementSer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = "__all__"
        
class PaymentSer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"