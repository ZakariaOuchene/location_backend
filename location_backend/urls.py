from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from location_api import views
from location_api.views import (ManagerView, CarView, PickupPointView, BookingView, TarifsView, ReviewView, ChildChairView)

router = routers.DefaultRouter()
router.register(r"managers", ManagerView, basename="managers")
router.register(r"cars", CarView, basename="cars")
router.register(r"pickup-point", PickupPointView, basename="pickup-point")
router.register(r"child-chair", ChildChairView, basename="child-chair")
router.register(r"booking", BookingView, basename="booking")
router.register(r"tarifs", TarifsView, basename="tarifs")
router.register(r"reviews", ReviewView, basename="reviews")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    
    path("token/manager/", views.ManagerTokenObtainPairView.as_view(),name="manager_token_obtain_pair"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
