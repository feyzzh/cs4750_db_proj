from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NutritionLogForm, SleepLogForm
from .models import NutritionLog, SleepLog

# Create your views here.
def home(request):
    return render(request, 'home.html')

# @login_required
def add_nutrition(request):
    if request.method == 'POST':
        form = NutritionLogForm(request.POST)
        if form.is_valid():
            nutrition_log = form.save(commit=False)
            nutrition_log.user = request.user
            nutrition_log.save()
            return redirect('nutrition_log_success')
    else:
        form = NutritionLogForm()

    return render(request, 'add_nutrition.html', {'form': form})


# @login_required
def add_sleep(request):
    if request.method == 'POST':
        form = SleepLogForm(request.POST)
        if form.is_valid():
            sleep_log = form.save(commit=False)
            sleep_log.user = request.user
            sleep_log.save()
            return redirect('home')
    else:
        form = SleepLogForm()

    return render(request, 'add_sleep.html', {'form': form})