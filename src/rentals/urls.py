from django.urls import path, re_path
from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet
from . import views



app_name = 'rentals'
router = DefaultRouter()
router.register(r'devices', DeviceViewSet)

urlpatterns = [
    path('',home,name='home'),

    path('products/',products,name='products'),
    path('products/<str:category_slug>/', category_devices, name='category_devices'),

    path('device/<int:device_id>/', device_detail, name='device_detail'),
    path('rental/<int:device_id>/payment/', payment_page, name='payment'),

    path('rental/<int:device_id>/confirm/', confirm_rental, name='confirm_rental'),
    path('order-summary/', order_summary, name='order_summary'), 

    path('search/', search_devices, name='search'),

    path('return/<int:rental_id>/', return_device, name='return_device'),
    path('available/<str:category_slug>/', similar_available_devices, name='available_devices'),
  
    path('', include(router.urls)),
]


