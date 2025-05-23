from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import NutritionLogForm, SleepLogForm, FitnessLogForm, FoodItemForm, GoalForm, NutritionGoalForm, \
    FitnessGoalForm, SleepGoalForm, EventForm
from .models import NutritionLog, SleepLog, FitnessLog, Goals, NutritionGoals, FitnessGoals, SleepGoals, Events, \
    EventParticipants

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Users
from .forms import SignupForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Avg, Count, Q
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime


def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data

            auth_user = User.objects.create_user(
                username=user_data['email'],  # Using email as username
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
            )

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
        username = request.POST.get('username')
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
        user_goals = Goals.objects.filter(user=custom_user).order_by('-start_time')
    except Users.DoesNotExist:
        return HttpResponse("No matching user found.", status=400)
 
    if request.method == "POST":
        # Only update fields if a new value is submitted
        for field in ['first_name', 'last_name', 'phone_number', 'city', 'state', 'country']:
            value = request.POST.get(field)
            if value and value != getattr(custom_user, field):
                setattr(custom_user, field, value)

        custom_user.save()
        return redirect('profile')
    
    return render(request, 'profile.html', {'profile': custom_user, 'goals': user_goals})

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
            return redirect('fit_dash')
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
            return redirect('sleep_dash')
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
def add_goal(request, goal_type):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if goal_type == 'nutrition':
            form = NutritionGoalForm(request.POST)
        elif goal_type == 'fitness':
            form = FitnessGoalForm(request.POST)
        elif goal_type == 'sleep':
            form = SleepGoalForm(request.POST)
        if form.is_valid():
            goals = form.save(commit=False)
            auth_user = request.user
            try:
                custom_user = Users.objects.get(email=auth_user.email)
            except Users.DoesNotExist:
                return HttpResponse("No matching user found.", status=400)

            goals.user = custom_user
            goals.goal_type=goal_type
            if goal_type not in ['wellness','sleep','fitness','nutrition']:
                goals.goal_type='wellness'
            goals.save()
            return redirect('home')
    else:
        form = GoalForm()
        if goal_type == 'nutrition':
            form = NutritionGoalForm()
        elif goal_type == 'fitness':
            form = FitnessGoalForm()
        elif goal_type == 'sleep':
            form = SleepGoalForm()
    return render(request, 'add_goal.html', {'form': form,'goal_type':goal_type})
@login_required
def add_goal_helper(request):
    return render(request, 'goal_helper.html')

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

    nutrition_logs_json = json.dumps(nutrition_logs_by_date, cls=DjangoJSONEncoder)

    nutrition_logs = NutritionLog.objects.filter(user=user).order_by('-time_of_consumption')

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

@login_required
def fitness_dashboard(request):
    user = Users.objects.get(email=request.user.email)
    selected_date_str = request.GET.get('date')
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date() if selected_date_str else timezone.localdate()
    except ValueError:
        selected_date = timezone.localdate()

    fitness_logs = FitnessLog.objects.filter(user=user).order_by('-start_time')

    grouped_logs = defaultdict(list)
    for log in fitness_logs:
        log_date = log.start_time.date()
        duration_minutes = int((log.end_time - log.start_time).total_seconds() // 60)  # Calculate duration
        grouped_logs[str(log_date)].append({
            'activity': log.activity, 
            'duration_minutes': duration_minutes,
            'time_of_workout': log.start_time.strftime('%Y-%m-%d %H:%M'),
        })

    recent_logs = fitness_logs[:10]

    day_logs = grouped_logs.get(str(selected_date), [])

    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    weekly_logs = []
    for i in range(7):
        date_str = str(start_of_week + timedelta(days=i))
        weekly_logs.extend(grouped_logs.get(date_str, []))
    total_duration_today = sum([log['duration_minutes'] for log in day_logs]) / 60
    total_duration_week = sum([log['duration_minutes'] for log in weekly_logs]) / 60

    weekly_hours_per_day = []
    for i in range(7):
        date = start_of_week + timedelta(days=i)
        logs = grouped_logs.get(str(date), [])
        total = sum([log['duration_minutes'] for log in logs]) / 60
        weekly_hours_per_day.append({'day': calendar.day_name[date.weekday()], 'hours': total})

    fitness_logs_by_date = json.dumps(grouped_logs)

    context = {
        'selected_date': selected_date,
        'fitness_logs': recent_logs,
        'fitness_logs_by_date': fitness_logs_by_date,
        'total_duration_today': total_duration_today,
        'total_duration_week': total_duration_week,
        'weekly_hours_per_day': weekly_hours_per_day,
    }

    return render(request, 'board_fitness.html', context)


@login_required
def sleep_dashboard(request):
    user = Users.objects.get(email=request.user.email)
    selected_date_str = request.GET.get('date')
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date() if selected_date_str else timezone.localdate()
    except ValueError:
        selected_date = timezone.localdate()

    sleep_logs_qs = SleepLog.objects.filter(user=user).order_by('-start_time')

    recent_logs = []
    for log in sleep_logs_qs[:10]:
        total_hours = round((log.end_time - log.start_time).total_seconds() / 3600, 2)
        recent_logs.append({
            'sleep_date': log.start_time.date(),
            'start_time': log.start_time.strftime('%Y-%m-%d %H:%M'),
            'end_time': log.end_time.strftime('%Y-%m-%d %H:%M'),
            'total_hours': total_hours,
        })

    grouped_logs = defaultdict(list)
    for log in sleep_logs_qs:
        log_date = log.start_time.date()
        total_hours = round((log.end_time - log.start_time).total_seconds() / 3600, 2)
        grouped_logs[str(log_date)].append({
            'start_time': log.start_time.strftime('%Y-%m-%d %H:%M'),
            'end_time': log.end_time.strftime('%Y-%m-%d %H:%M'),
            'total_hours': total_hours,
        })

    sleep_logs_by_date = json.dumps(grouped_logs)

    context = {
        'sleep_logs': recent_logs,
        'sleep_logs_by_date': sleep_logs_by_date,
        'selected_date': selected_date,
    }
    return render(request, 'board_sleep.html', context)

@login_required
def entry_manager(request):
    user_email = request.user.email
    try:
        user = Users.objects.get(email=user_email)
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found.'})

    nutrition_logs = NutritionLog.objects.select_related('food').filter(user_id=user)
    fitness_logs = FitnessLog.objects.filter(user_id=user)
    sleep_logs = SleepLog.objects.filter(user_id=user)

    return render(request, 'entry_manager.html', {
        'nutrition_logs': nutrition_logs,
        'fitness_logs': fitness_logs,
        'sleep_logs': sleep_logs,
    })


@login_required
def goals_manager(request):
    user_email = request.user.email
    try:
        user = Users.objects.get(email=user_email)
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found.'})

    nutrition_goals = NutritionGoals.objects.select_related('goals_ptr', 'food').filter(goals_ptr__user_id=user.user_id)
    fitness_goals = FitnessGoals.objects.select_related('goals_ptr').filter(goals_ptr__user_id=user.user_id)
    sleep_goals = SleepGoals.objects.select_related('goals_ptr').filter(goals_ptr__user_id=user.user_id)
    wellness_goals = Goals.objects.filter(user_id=user.user_id, goal_type='wellness')

    return render(request, 'goal_manager.html', {
        'nutrition_goals': nutrition_goals,
        'fitness_goals': fitness_goals,
        'sleep_goals': sleep_goals,
        'wellness_goals': wellness_goals,
    })


@login_required
def view_goals(request):
    user_email = request.user.email

    try:
        user = Users.objects.get(email=user_email)
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found.'})

    goals = Goals.objects.filter(user=user).order_by('-start_time')
    nutrition_goals = NutritionGoals.objects.filter(user=user).order_by('-start_time')
    fitness_goals = FitnessGoals.objects.filter(user=user).order_by('-start_time')
    sleep_goals = SleepGoals.objects.filter(user=user).order_by('-start_time')
    nutrition_goal_info=[]
    fitness_goal_info=[]
    sleep_goal_info=[]
    for goal in nutrition_goals:
        food_logs = NutritionLog.objects.filter(
            user=goal.user,
            time_of_consumption__gte=goal.start_time,
            time_of_consumption__lte=goal.end_time,
        )
        if goal.food:
            food_logs = food_logs.filter(food=goal.food)
        total_grams = food_logs.aggregate(total_grams=Sum('num_grams_consumed'))['total_grams']
        if total_grams is None:
            total_grams = 0
        if total_grams < goal.lower_grams:
            progress = (total_grams / goal.lower_grams) * 100
            status = "Under"
        elif goal.lower_grams <= total_grams <= goal.upper_grams:
            progress = 100
            status = "On Target"
        else:
            progress = 100 + ((total_grams - goal.upper_grams) / goal.upper_grams) * 100 #how far over max we are
            status = "Over"
        nutrition_goal_info.append({'goal': goal, 'progress': "{:.2f}".format(progress), 'status': status})
    for goal in fitness_goals:
        activities = FitnessLog.objects.filter(
            user=goal.user,
            start_time__gte=goal.start_time,  # find activities somewhere in goal's time
            end_time__lte=goal.end_time,
        )
        if goal.activity:
            activities = activities.filter(activity=goal.activity)
        total_minutes = sum(
            (activity.end_time - activity.start_time).total_seconds() / 60
            for activity in activities
        )
        if total_minutes is None:
            total_minutes = 0
        progress = (total_minutes / goal.target_minutes) * 100
        fitness_goal_info.append({'goal':goal,'progress':"{:.2f}".format(progress)})
    for goal in sleep_goals:
        sleeps = SleepLog.objects.filter(
            user=goal.user,
            start_time__gte=goal.start_time,  # find activities somewhere in goal's time
            end_time__lte=goal.end_time,
        )
        total_hours = sum(
            (sleep.end_time - sleep.start_time).total_seconds() / 60
            for sleep in sleeps
        ) /60
        if total_hours is None:
            total_hours = 0
        progress = (total_hours / float(goal.target_hours)) * 100
        total_quality = sum(sleep.sleep_quality for sleep in sleeps)
        count = sleeps.count()
        avg_quality = total_quality / count if count > 0 else 0
        avg_10 = avg_quality * 10
        target_10 = goal.target_quality * 10
        sleep_goal_info.append({'goal': goal, 'progress': "{:.2f}".format(progress),
                                'avg_quality': "{:.2f}".format(avg_quality),
                               'avg_10':avg_10,'target_10': target_10}
                               )
    context={
        'goals': goals,
        'nutrition_goals': nutrition_goal_info,
        'fitness_goals': fitness_goal_info,
        'sleep_goals': sleep_goal_info
    }
    return render(request, 'goals.html', context)

@login_required
def toggle_goal(request, goal_id):
    if request.method == 'POST':
        try:
            auth_user = request.user
            custom_user = Users.objects.get(email=auth_user.email)
            goal = get_object_or_404(Goals, goal_id=goal_id, user=custom_user)
            goal.completed = not goal.completed
            goal.save()
            return redirect('profile')
        except Exception as e:
            return redirect('profile')

@login_required
def delete_goal(request, goal_id):
    if request.method == 'POST':
        try:
            auth_user = request.user
            custom_user = Users.objects.get(email=auth_user.email)
            goal = get_object_or_404(Goals, goal_id=goal_id, user=custom_user)
            goal.delete()
            return redirect('profile')
        except Exception as e:
            return redirect('profile')

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            auth_user = request.user
            try:
                custom_user = Users.objects.get(email=auth_user.email)
            except Users.DoesNotExist:
                return HttpResponse("No matching user found.", status=400)

            event.host = custom_user
            event.save()
            EventParticipants.objects.create(event=event, participant=custom_user)
            return redirect('home')
    else:
        form = EventForm()

    return render(request, 'add_event.html', {'form': form})

@login_required
def view_events(request):
    user_email = request.user.email
    try:
        user = Users.objects.get(email=user_email)
    except Users.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found.'})
    events = Events.objects.order_by('-start_time')
    hosted_events = Events.objects.filter(host=user)
    enrolled_events = EventParticipants.objects.filter(participant=user)
    context = {
        'events': events,
        'hosted': hosted_events,
        'enrolled': enrolled_events
    }
    return render(request, 'events.html', context)

@login_required
def enroll(request):
    if request.method == 'POST':
        user_email = request.user.email
        try:
            user = Users.objects.get(email=user_email)
        except Users.DoesNotExist:
            return render(request, 'error.html', {'message': 'User not found.'})
        event_id = request.POST.get('enroll_event_id')
        event = Events.objects.get(event_id=event_id)
        if not EventParticipants.objects.filter(event=event, participant=user).exists():
            EventParticipants.objects.create(event=event, participant=user)
        return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def delete_event(request):
    if request.method == "POST":
        user_email = request.user.email
        try:
            user = Users.objects.get(email=user_email)
        except Users.DoesNotExist:
            return render(request, 'error.html', {'message': 'User not found.'})
        event_id = request.POST.get("delete_event_id")
        event = Events.objects.get(event_id=event_id)
        if event.host == user:
            event.delete()
            messages.success(request, "Event deleted successfully.")
        else:
            messages.error(request, "You do not have permission to delete this event.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def resolve_event(request):
    if request.method == "POST":
        event_id = request.POST.get("resolve_event_id")
        event = Events.objects.get(event_id=event_id)
        participants = EventParticipants.objects.filter(event=event)
        for participant in participants:
            FitnessLog.objects.create(
                user=participant.participant,
                activity=event.activity,
                start_time=event.start_time,
                end_time=event.end_time,
                description=event.description
            )
        event.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))