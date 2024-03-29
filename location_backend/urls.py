from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

from location_api import views
from location_api.views import (ManagerView, CarView, PickupPointView, BookingView, TarifsView, ReviewView)

router = routers.DefaultRouter()
router.register(r"managers", ManagerView, basename="managers")
router.register(r"cars", CarView, basename="cars")
router.register(r"pickup-point", PickupPointView, basename="pickup-point")
router.register(r"booking", BookingView, basename="booking")
router.register(r"tarifs", TarifsView, basename="tarifs")
router.register(r"reviews", ReviewView, basename="reviews")

urlpatterns = [
    # path('', RedirectView.as_view(url='/admin/login/?next=/'), name='root_redirect'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path("auth/user/", views.UserDetailsAPIView.as_view(), name="user_detail"),
    path("user_update/<int:user_id>/", views.update_user, name="update_user"),
    path("user_image_update/<int:user_id>/",
         views.update_user_image, name="update_user_image"),
    path('change_password/<int:userId>/',
         views.change_password, name='change_password'),
    path("token/manager/", views.ManagerTokenObtainPairView.as_view(),name="manager_token_obtain_pair"),
    
    path("tarif/car/<int:id_car>/",
         views.TarifByCaryView.as_view(), name="get_tarif_by_car"),
    
    path('booking-sur-place/', views.BookingSurPlace.as_view(), name='booking_sur_place'),
    
    path('booking-en-ligne/', views.BookingEnLigne.as_view(), name='booking_en_ligne'),
    
    path('booking-archive/', views.BookingArchive.as_view(), name='booking_archive'),
    
    path('booking/update-paiement/<int:booking_id>/', views.update_paiement_booking, name='update_paiement_booking'),
    
    path('booking/update-repaiement/<int:booking_id>/', views.update_repaiement_booking, name='update_repaiement_booking'),
    
    path('booking/update-archive/<int:booking_id>/', views.update_archive_booking, name='update_archive_booking'),
    
    path('car/update-dispo-car/<int:car_id>/', views.update_dispo_car, name='update_dispo_car'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
