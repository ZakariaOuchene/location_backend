from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from location_api import views
from location_api.views import (UserView, ManagerView, CarView, CarImageView, PickupPointView, BookingView, TarifsView, PaiementView, PaymentView)

router = routers.DefaultRouter()
router.register(r"managers", ManagerView, basename="managers")
router.register(r"users", UserView, basename="users")
router.register(r"cars", CarView, basename="cars")
router.register(r"images-car", CarImageView)
router.register(r"pickup-point", PickupPointView, basename="pickup-point")
router.register(r"booking", BookingView, basename="booking")
router.register(r"tarifs", TarifsView, basename="tarifs")
router.register(r"card-paiement", PaiementView, basename="card-paiement")
router.register(r"paiemnet-booking", PaymentView, basename="paiemnet-booking")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
