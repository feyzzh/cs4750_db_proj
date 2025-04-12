from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NutritionLogForm, SleepLogForm, FitnessLogForm
from .models import NutritionLog, SleepLog, FitnessLog


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Users
from .forms import SignupForm
from django.contrib import messages
from django.http import HttpResponse

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