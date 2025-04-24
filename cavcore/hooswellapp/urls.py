from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add_food', views.add_food, name='add_food'),
    path('add_nutrition', views.add_nutrition, name='add_nutrition'),
    path('add_sleep', views.add_sleep, name='add_sleep'),
    path('add_fitness', views.add_fitness_log, name='add_fitness_log'),
    path('add_goal', views.add_goal, name='add_goal'),
    path('stats/', views.stats_dashboard, name='stats_dashboard'),
    path('nutri-dash/', views.nutrition_dashboard, name='nutri_dash'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('goals/', views.view_goals, name='goals'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('entry_manager/', views.entry_manager, name='entry_manager'),
    path('update_entry/', views.update_entry, name='update_entry'),
    path('delete_entry/', views.delete_entry, name='delete_entry'),
    path('toggle_goal/<int:goal_id>/', views.toggle_goal, name='toggle_goal'),
    path('delete_goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
]