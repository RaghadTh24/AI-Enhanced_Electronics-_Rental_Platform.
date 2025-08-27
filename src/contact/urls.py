from django.urls import path, re_path
from .views import *
from . import views


app_name = 'contact'

urlpatterns = [
    path('',contact_us,name='contact_us'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),


]