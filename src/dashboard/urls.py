from django.urls import path, re_path
from .views import manager_dashboard
from .views import *
from .views import submit_review
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('seller/', seller_dashboard, name='seller_dashboard'),
    path('my_devices/', seller_products, name='seller_products'),
    path('add_device/', add_device, name='add_device'),
    path('modify/<int:device_id>/', modify_device, name='modify_device'),
    path('delete/<int:device_id>/', delete_device, name='delete_device'),
    path('modify-by-input/', modify_device_by_input, name='modify_device_by_input'),
    path('delete-by-input/', delete_device_by_input, name='delete_device_by_input'),
    path('confirm-return/<int:rental_id>/<str:decision>/', views.confirm_return, name='confirm_return'),





    path('manager/', manager_sentiment_dashboard, name='manager_dashboard'),
    path('manage/users/', manage_users, name='manage_users'),
    path('delete/user/<int:user_id>/', delete_user, name='delete_user'),
    path('manage/devices/', manage_devices, name='manage_devices'),
    path('delete/device/<int:device_id>/', delete_device_admin, name='delete_device_admin'),




    path('buyer/', buyer_dashboard, name='buyer_dashboard'),
    path('rate/<int:device_id>/', rate_device, name='rate_device'),
    path('submit_review/', submit_review, name='submit_review'),
    path('my-rentals/', my_rentals, name='my_rentals'),
    path('mark_returned/<int:rental_id>/', mark_as_returned, name='mark_as_returned'),
]