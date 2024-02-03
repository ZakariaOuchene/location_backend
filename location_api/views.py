from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import PermissionDenied
from .models import User, Manager, Car, PickupPoint, Booking, Tarifs, Review
from .serializers import UserSer, ManagerSer, CarSer, PickupPointSer, BookingSer, TarifsSer
from .serializers import ReviewSer
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.db.models import Sum, F
from django.core.exceptions import ObjectDoesNotExist
import logging
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models.functions import TruncMonth, TruncYear

logger = logging.getLogger(__name__)

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
    
# class UserDetailsAPIView(APIView):
#     permission_classes = [IsAuthenticatedOrDenied]

#     def get(self, request):
#         user = request.user
#         serializer = UserSer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserDetailsAPIView(APIView):
    # permission_classes = [IsAuthenticatedOrDenied]
    permission_classes = [IsAuthenticatedOrDenied]

    def get(self, request):
        user = request.user
        serializer = UserSer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    
    @action(detail=False, methods=['get'])
    def total_cars(self, request):
        total_cars = Car.objects.count()
        return Response({'total_cars': total_cars})
    
class TarifByCaryView(APIView):
    def get(self, request, id_car):
        # Retrieve the properties for the given category id
        print("Received poid ID:", id_car)
        tarif = Tarifs.objects.filter(car=id_car)
        serializer = TarifsSer(tarif, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PickupPointView(viewsets.ModelViewSet):
    queryset = PickupPoint.objects.all()
    serializer_class = PickupPointSer

class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSer
    
    @action(detail=False, methods=['get'])
    def total_booking_surplace(self, request):
        total_booking_surplace = Booking.objects.filter(surPlace=True, repayment=False).count()
        return Response({'total_booking_surplace': total_booking_surplace})
    
    @action(detail=False, methods=['get'])
    def total_reviews_enligne(self, request):
        total_reviews_enligne = Booking.objects.filter(surPlace=False, repayment=False).count()
        return Response({'total_reviews_enligne': total_reviews_enligne})
    
    @action(detail=False, methods=['get'])
    def total_revenue(self, request):
        total_paiement_sur_place = Booking.objects.filter(surPlace=True, payement=True, repayment=False).aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_paiement_en_ligne = Booking.objects.filter(surPlace=False, payement=True, repayment=False).aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_paiement = Booking.objects.filter(payement=True, repayment=False).aggregate(Sum('total_price'))['total_price__sum'] or 0

        response_data = {
            'total_paiement_sur_place': total_paiement_sur_place,
            'total_paiement_en_ligne': total_paiement_en_ligne,
            'total_paiement': total_paiement,
        }

        return Response(response_data)
    
    @action(detail=False, methods=["get"])
    def total_frais_surplace_by_month(self, request):
        # Obtenez l'année à partir des paramètres de requête ou utilisez l'année actuelle par défaut
        year = request.GET.get('year', timezone.now().year)
        # Utilisez la fonction aggregate pour calculer la somme des fraisElbal par mois
        frais_surplace_by_month = (
            Booking.objects
            # Filtrez les booking
            .filter(payement=True, surPlace=True, date_book__year=year)
            .annotate(month=TruncMonth('date_book'))
            .values('month')
            .annotate(total_frais_surplace=Sum(F('total_price_HT')))
            .order_by('month')
        )
        # Sérialisez les données
        data = [{'month': entry['month'].strftime(
            '%m'), 'total_frais_surplace': entry['total_frais_surplace']} for entry in frais_surplace_by_month]

        return JsonResponse(data, safe=False)
    
    @action(detail=False, methods=["get"])
    def total_frais_surplace_by_year(self, request):
        # Utilisez la fonction aggregate pour calculer la somme des fraisElbal par mois
        frais_surplace_by_year = (
            Booking.objects
            # Filtrez les booking
            .filter(payement=True, surPlace=True)
            .annotate(year=TruncYear('date_book'))
            .values('year')
            .annotate(total_frais_surplace=Sum(F('total_price_HT')))
            .order_by('year')
        )
        # Sérialisez les données
        data = [{'year': entry['year'].strftime(
            '%Y'), 'total_frais_surplace': entry['total_frais_surplace']} for entry in frais_surplace_by_year]

        return JsonResponse(data, safe=False)
    
    @action(detail=False, methods=["get"])
    def total_frais_enligne_by_month(self, request):
        # Obtenez l'année à partir des paramètres de requête ou utilisez l'année actuelle par défaut
        year = request.GET.get('year', timezone.now().year)
        # Utilisez la fonction aggregate pour calculer la somme des fraisElbal par mois
        frais_enligne_by_month = (
            Booking.objects
            # Filtrez les booking
            .filter(payement=True, surPlace=False, repayment=False, date_book__year=year)
            .annotate(month=TruncMonth('date_book'))
            .values('month')
            .annotate(total_frais_enligne=Sum(F('total_price_HT')))
            .order_by('month')
        )
        # Sérialisez les données
        data = [{'month': entry['month'].strftime(
            '%m'), 'total_frais_enligne': entry['total_frais_enligne']} for entry in frais_enligne_by_month]

        return JsonResponse(data, safe=False)
    
    @action(detail=False, methods=["get"])
    def total_frais_enligne_by_year(self, request):
        # Utilisez la fonction aggregate pour calculer la somme des fraisElbal par mois
        frais_enligne_by_year = (
            Booking.objects
            # Filtrez les booking
            .filter(payement=True, surPlace=False, repayment=False)
            .annotate(year=TruncYear('date_book'))
            .values('year')
            .annotate(total_frais_enligne=Sum(F('total_price_HT')))
            .order_by('year')
        )
        # Sérialisez les données
        data = [{'year': entry['year'].strftime(
            '%Y'), 'total_frais_enligne': entry['total_frais_enligne']} for entry in frais_enligne_by_year]

        return JsonResponse(data, safe=False)
    
    @action(detail=False, methods=["get"])
    def total_frais_all_by_month(self, request):
        # Obtenez l'année à partir des paramètres de requête ou utilisez l'année actuelle par défaut
        year = request.GET.get('year', timezone.now().year)
        # Utilisez la fonction aggregate pour calculer la somme des fraisElbal par mois
        frais_all_by_month = (
            Booking.objects
            # Filtrez les booking
            .filter(payement=True, repayment=False, date_book__year=year)
            .annotate(month=TruncMonth('date_book'))
            .values('month')
            .annotate(total_frais_all=Sum(F('total_price_HT')))
            .order_by('month')
        )
        # Sérialisez les données
        data = [{'month': entry['month'].strftime(
            '%m'), 'total_frais_all': entry['total_frais_all']} for entry in frais_all_by_month]

        return JsonResponse(data, safe=False)
    
    @action(detail=False, methods=["get"])
    def total_frais_all_by_year(self, request):
        # Utilisez la fonction aggregate pour calculer la somme des fraisElbal par mois
        frais_all_by_year = (
            Booking.objects
            # Filtrez les booking
            .filter(payement=True, repayment=False)
            .annotate(year=TruncYear('date_book'))
            .values('year')
            .annotate(total_frais_all=Sum(F('total_price_HT')))
            .order_by('year')
        )
        # Sérialisez les données
        data = [{'year': entry['year'].strftime(
            '%Y'), 'total_frais_all': entry['total_frais_all']} for entry in frais_all_by_year]

        return JsonResponse(data, safe=False)
    
class BookingArchive(APIView):
    def get(self, request, *args, **kwargs):
        booking_archive = Booking.objects.filter(archive=True).order_by('-date_book')
        serializer = BookingSer(booking_archive, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BookingSurPlace(APIView):
    def get(self, request, *args, **kwargs):
        booking_sur_place = Booking.objects.filter(surPlace=True, archive=False).order_by('-date_book')
        serializer = BookingSer(booking_sur_place, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BookingEnLigne(APIView):
    def get(self, request, *args, **kwargs):
        booking_en_ligne = Booking.objects.filter(surPlace=False, archive=False).order_by('-date_book')
        serializer = BookingSer(booking_en_ligne, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def update_paiement_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        booking.payement = not booking.payement  # Toggle the etat field
        booking.save(update_fields=['payement'])

        serializer = BookingSer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def update_repaiement_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        booking.repayment = not booking.repayment  # Toggle the etat field
        booking.save(update_fields=['repayment'])

        serializer = BookingSer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def update_archive_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        booking.archive = not booking.archive  # Toggle the etat field
        booking.save(update_fields=['archive'])

        serializer = BookingSer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

class TarifsView(viewsets.ModelViewSet):
    queryset = Tarifs.objects.all()
    serializer_class = TarifsSer

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSer
    
    @action(detail=False, methods=['get'])
    def total_reviews(self, request):
        total_reviews = Review.objects.count()
        return Response({'total_reviews': total_reviews})
    
@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def update_dispo_car(request, car_id):
    try:
        car = Car.objects.get(id_car=car_id)
    except Car.DoesNotExist:
        return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        car.disponible = not car.disponible  # Toggle the etat field
        car.save(update_fields=['disponible'])

        serializer = CarSer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)