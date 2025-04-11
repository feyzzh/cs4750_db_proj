from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_nutrition', views.add_nutrition, name='add_nutrition'),
    path('add_sleep', views.add_sleep, name='add_sleep'),
]