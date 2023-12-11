from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import PermissionDenied
from .models import User, Manager, Car, PickupPoint, Booking, Tarifs, Paiement, Payment, Review, Client
from .serializers import UserSer, ManagerSer, CarSer, PickupPointSer, BookingSer, TarifsSer, PaiementSer, PaymentSer, ClientSer
from .serializers import ReviewSer

class IsAuthenticatedOrDenied(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        else:
            raise PermissionDenied(
                "You must be authenticated to access this view.")
            
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSer
    
class ClientView(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSer

class ManagerView(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSer
    
class ManagerTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        email = request.data.get("email")
        password = request.data.get("password")

        Usercode = User.objects.get(email=email)
        user = Usercode.manager

        code = user.code

        if check_password(password, Usercode.password):
            code = Usercode.code

        else:
            code = "123"
            return Response(
                {"message": "Mot de passe incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.select_related("manager").get(code=code)
            manager = user.manager

            if manager and manager.etat:
                if check_password(password, user.password):
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            "access": str(refresh.access_token),
                            "role": manager.role,
                            "refresh": str(refresh),
                            "firstName": user.first_name,  # Use first_name field
                            "lastName": user.last_name,
                            "email": user.email,
                            "id": user.id,
                        }
                    )
                else:
                    return Response(
                        {"message": "Mot de passe incorrect"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "votre compte est désactivé"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except User.DoesNotExist:

            return Response(
                {"message": "Email incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class CarView(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSer

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

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSer