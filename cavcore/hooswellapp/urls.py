from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_nutrition', views.add_nutrition, name='add_nutrition'),
    path('add_sleep', views.add_sleep, name='add_sleep'),
    path('add_fitness', views.add_fitness_log, name='add_fitness_log'),
    path('stats/', views.stats_dashboard, name='stats_dashboard'),
    path('nutri-dash/', views.nutrition_dashboard, name='nutri_dash'),
    path('dashboard/', views.dashboard, name='dashboard')

]