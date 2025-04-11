from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_nutrition', views.add_nutrition, name='add_nutrition'),
    path('add/', views.add_fitness_log, name='add_fitness_log'),
    path('view/', views.view_fitness_logs, name='view_fitness_logs'),
    
]