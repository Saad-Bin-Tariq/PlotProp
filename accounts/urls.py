from django.urls import path
from .views import *


urlpatterns = [
    path('',home),
    path('home/',home,name='name'),
    path('register/',register, name='register'),
    path('login/',login, name='login'),
    path('logout/',logout, name='logout'),
    path('plotfinder/',plotfinder, name='plotfinder'),
    path('pricefinder/',pricefinder, name='pricefinder'),
    path('data/',data, name='data'),
    path('sales/',sales, name='sales'),
    path('add-sale/',add_sale, name='add_sale'),
    path('get_data/', get_data, name='get_data'),

]