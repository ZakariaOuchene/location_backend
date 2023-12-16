from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import PermissionDenied
from .models import User, Manager, Car, PickupPoint, Booking, Tarifs, Review, ChildChair
from .serializers import UserSer, ManagerSer, CarSer, PickupPointSer, BookingSer, TarifsSer, ChildChairSer
from .serializers import ReviewSer
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse

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

            if manager :
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

@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
def update_user(request, user_id):

    user = User.objects.get(id=user_id)
    user.first_name = request.data.get("first_name", user.first_name)
    user.last_name = request.data.get("last_name", user.last_name)
    user.gender = request.data.get("gender", user.gender)
    user.tel = request.data.get("tel", user.tel)
    user.ville = request.data.get("ville", user.ville)
    
    user.save(update_fields=["first_name", "last_name","gender", "tel", "ville"])
    return Response(
        {"message": "User data updated successfully."}, status=status.HTTP_200_OK
    )
    
@api_view(["PUT"])
# @permission_classes([IsAuthenticated])
def update_user_image(request, user_id):
    user = User.objects.get(id=user_id)
    user.image = request.data.get("image", user.image)
    user.save(update_fields=['image'])
    return Response(
        {"message": "User image updated successfully."}, status=status.HTTP_200_OK
    )
    

@api_view(["PUT"])
#@permission_classes([IsAuthenticated])
def change_password(request, userId):
    user = User.objects.get(id=userId)
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    if check_password(old_password, user.password):
        if new_password == confirm_password:
            user.password = new_password
            user.save()
            return JsonResponse(
                {"success": True, "message": "Mot de passe mis à jour avec succès."}
            )
        else:
            return JsonResponse(
                {"error": "Le nouveau mot de passe et le mot de passe de confirmation ne correspondent pas."}
            )
    else:
        return JsonResponse({"error": "L’ancien mot de passe est incorrect."})
    
class CarView(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSer

class PickupPointView(viewsets.ModelViewSet):
    queryset = PickupPoint.objects.all()
    serializer_class = PickupPointSer
    
class ChildChairView(viewsets.ModelViewSet):
    queryset = ChildChair.objects.all()
    serializer_class = ChildChairSer

class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSer

class TarifsView(viewsets.ModelViewSet):
    queryset = Tarifs.objects.all()
    serializer_class = TarifsSer

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSer