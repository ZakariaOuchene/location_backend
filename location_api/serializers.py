from rest_framework import serializers

from .models import User, Manager, Car, PickupPoint, Booking, Tarifs, Review

class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ManagerSer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = "__all__"

class CarSer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

class PickupPointSer(serializers.ModelSerializer):
    class Meta:
        model = PickupPoint
        fields = "__all__"

class BookingSer(serializers.ModelSerializer):
    name_pickup_start = serializers.CharField(source='pickup_start.lieu', read_only=True)
    name_pickup_end = serializers.CharField(source='pickup_end.lieu', read_only=True)
    name_car = serializers.CharField(source='car.model', read_only=True)
    
    class Meta:
        model = Booking
        fields = "__all__"

class TarifsSer(serializers.ModelSerializer):
    class Meta:
        model = Tarifs
        fields = "__all__"

class ReviewSer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
