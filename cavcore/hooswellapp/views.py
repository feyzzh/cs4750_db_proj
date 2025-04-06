from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NutritionLogForm
from .models import NutritionLog

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
