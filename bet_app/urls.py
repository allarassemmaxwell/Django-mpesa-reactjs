from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('place_bet/', views.place_bet, name='place_bet'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
]
