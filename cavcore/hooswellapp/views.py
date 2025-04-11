from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NutritionLogForm, FitnessLogForm
from .models import NutritionLog, FitnessLog

# Create your views here.
def home(request):
    return render(request, 'home.html')

# @login_required
def add_nutrition(request):
    if request.method == 'POST':
        form = NutritionLogForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            nutrition_log = form.save(commit=False)
            nutrition_log.user = request.user  # Set the current logged-in user
            nutrition_log.save()
            return redirect('nutrition_log_success')  # Redirect to success page
    else:
        form = NutritionLogForm()

    return render(request, 'add_nutrition.html', {'form': form})

def add_fitness_log(request):
    if request.method == 'POST':
        form = FitnessLogForm(request.POST)
        if form.is_valid():
            fitness_log = form.save(commit=False)
            fitness_log.user = request.user
            fitness_log.save()
            return redirect('view_fitness_logs')
    else:
        form = FitnessLogForm()

    return render(request, 'template/add_fitness_log.html', {'form': form})

@login_required
def view_fitness_logs(request):
    logs = FitnessLog.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'template/view_fitness_logs.html', {'logs': logs})