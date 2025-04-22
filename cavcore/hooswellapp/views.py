from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NutritionLogForm, SleepLogForm, FitnessLogForm, FoodItemForm, GoalForm
from .models import NutritionLog, SleepLog, FitnessLog


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Users
from .forms import SignupForm
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Avg, Count

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data

            # Create auth_user entry
            auth_user = User.objects.create_user(
                username=user_data['email'],  # Using email as username
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
            )

            # Create Users entry
            Users.objects.create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                phone_number=user_data['phone_number'],
                city=user_data['city'],
                state=user_data['state'],
                country=user_data['country'],
            )

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Will be email in this setup
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You’ve been logged out successfully.")
    return redirect('login')

@login_required
def profile(request):
    auth_user = request.user
    try:
        custom_user = Users.objects.get(email=auth_user.email)
    except Users.DoesNotExist:
        return HttpResponse("No matching user found.", status=400)

    return render(request, 'profile.html', {'profile': custom_user})

@login_required
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            auth_user = request.user
            try:
                custom_user = Users.objects.get(email=auth_user.email)
            except Users.DoesNotExist:
                return HttpResponse("No matching user found.", status=400)

            food_item.user = custom_user
            food_item.save()
            return redirect('nutri_dash')
    else:
        form = FoodItemForm()

    return render(request, 'add_food.html', {'form': form})

@login_required
def add_nutrition(request):
    if request.method == 'POST':
        form = NutritionLogForm(request.POST)
        if form.is_valid():
            nutrition_log = form.save(commit=False)
            auth_user = request.user
            try:
                custom_user = Users.objects.get(email=auth_user.email)
            except Users.DoesNotExist:
                return HttpResponse("No matching user found.", status=400)

            nutrition_log.user = custom_user
            nutrition_log.save()
            return redirect('home')
    else:
        form = NutritionLogForm()

    return render(request, 'add_nutrition.html', {'form': form})


@login_required
def add_sleep(request):
    if request.method == 'POST':
        form = SleepLogForm(request.POST)
        if form.is_valid():
            sleep_log = form.save(commit=False)
            auth_user = request.user
            try:
                custom_user = Users.objects.get(email=auth_user.email)
            except Users.DoesNotExist:
                return HttpResponse("No matching user found.", status=400)

            sleep_log.user = custom_user
            sleep_log.save()
            return redirect('home')
    else:
        form = SleepLogForm()

    return render(request, 'add_sleep.html', {'form': form})

@login_required
def add_fitness_log(request):
    if request.method == 'POST':
        form = FitnessLogForm(request.POST)
        if form.is_valid():
            fitness_log = form.save(commit=False)
            auth_user = request.user
            try:
                custom_user = Users.objects.get(email=auth_user.email)
            except Users.DoesNotExist:
                return HttpResponse("No matching user found.", status=400)

            fitness_log.user = custom_user
            fitness_log.save()
            return redirect('home')
    else:
        form = FitnessLogForm()

    return render(request, 'add_fitness_log.html', {'form': form})

from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goals = form.save(commit=False)
            auth_user = request.user
            try:
                custom_user = Users.objects.get(email=auth_user.email)
            except Users.DoesNotExist:
                return HttpResponse("No matching user found.", status=400)

            goals.user = custom_user
            goals.save()
            return redirect('home')
    else:
        form = GoalForm()
    return render(request, 'add_goal.html', {'form': form})

@login_required
def stats_dashboard(request):
    user_email = request.user.email

    try:
        user = Users.objects.get(email=user_email)
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found.'})

    nutrition_logs = NutritionLog.objects.filter(user=user).order_by('-time_of_consumption')
    nutrition_stats = NutritionLog.objects.filter(user=user).values('food').annotate(
        total_grams=Sum('num_grams_consumed'),
        # total_entries=Count('pk'),
    )

    fitness_logs = FitnessLog.objects.filter(user=user).order_by('-start_time')
    fitness_stats = FitnessLog.objects.filter(user=user).values('activity', 'start_time', 'end_time')

    sleep_logs = SleepLog.objects.filter(user=user).order_by('-start_time')
    sleep_stats = SleepLog.objects.filter(user=user).values('start_time', 'end_time', 'sleep_quality')

    # today's nutrition logs
    today = timezone.localtime().date()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())

    nutrition_logs_today = NutritionLog.objects.filter(
        user=user,
        time_of_consumption__range=(start, end)
    )

    total_grams_today = nutrition_logs_today.aggregate(
        total=Sum('num_grams_consumed')
    )['total'] or 0

    context = {
        'nutrition_logs': nutrition_logs,
        'nutrition_stats': nutrition_stats,
        'fitness_logs': fitness_logs,
        'fitness_stats': fitness_stats,
        'sleep_logs': sleep_logs,
        'sleep_stats': sleep_stats,

        'nutrition_logs_today': nutrition_logs_today,
        'total_grams_today': total_grams_today,
    }

    return render(request, 'stats_dashboard.html', context)


@login_required
def dashboard(request):

    user_email = request.user.email
    try:
        user = Users.objects.get(email=user_email)
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found.'})

    context = {

    }

    return render(request, 'dashboard.html', context)

from datetime import datetime, timedelta
from collections import defaultdict
import json

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder

from .models import NutritionLog, Users

import calendar


@login_required
def nutrition_dashboard(request):
    user = Users.objects.get(email=request.user.email)

    # Parse the selected date from query param (?date=YYYY-MM-DD), fallback to today
    selected_date_str = request.GET.get('date')
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date() if selected_date_str else timezone.localdate()
    except ValueError:
        selected_date = timezone.localdate()

    # Get all nutrition logs for this user
    nutrition_logs = NutritionLog.objects.filter(user=user).select_related('food').order_by('-time_of_consumption')

    # Group logs by date
    def group_logs_by_date(logs):
        grouped = defaultdict(list)
        for log in logs:
            log_date = log.time_of_consumption.date()
            grouped[str(log_date)].append({
                'food': log.food.food_item if log.food else '',
                'num_grams_consumed': log.num_grams_consumed,
                'time_of_consumption': log.time_of_consumption.strftime('%H:%M'),
            })
        return grouped

    nutrition_logs_by_date = group_logs_by_date(nutrition_logs)

    # Logs for the selected day
    day_logs = nutrition_logs_by_date.get(str(selected_date), [])
    total_grams_today = sum(entry['num_grams_consumed'] for entry in day_logs)

    # Logs for the selected week
    start_of_week = selected_date - timedelta(days=selected_date.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    weekly_logs = []
    for offset in range(7):
        date_str = str(start_of_week + timedelta(days=offset))
        if date_str in nutrition_logs_by_date:
            weekly_logs.extend(nutrition_logs_by_date[date_str])

    total_grams_week = sum(entry['num_grams_consumed'] for entry in weekly_logs)

    # Serialize grouped logs for JavaScript
    nutrition_logs_json = json.dumps(nutrition_logs_by_date, cls=DjangoJSONEncoder)

    nutrition_logs = NutritionLog.objects.filter(user=user).order_by('-time_of_consumption')

    # Calculate the weekly grams per day
    weekly_grams_per_day = []

    for offset in range(7):
        current_date = start_of_week + timedelta(days=offset)
        date_str = str(current_date)
        day_name = calendar.day_name[current_date.weekday()]  # e.g., 'Monday'

        logs_for_day = nutrition_logs_by_date.get(date_str, [])
        total_grams = sum(entry['num_grams_consumed'] for entry in logs_for_day)

        weekly_grams_per_day.append({
            'day': day_name,
            'grams': total_grams
        })


    context = {
        'selected_date': selected_date,
        'total_grams_today': total_grams_today,
        'total_grams_week': total_grams_week,
        'nutrition_logs_by_date': nutrition_logs_json,
        'nutrition_logs': nutrition_logs,
        'weekly_grams_per_day': weekly_grams_per_day,
    }

    return render(request, 'board_nutrition.html', context)
