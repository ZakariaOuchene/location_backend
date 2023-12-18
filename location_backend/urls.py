from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

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
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    
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
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
