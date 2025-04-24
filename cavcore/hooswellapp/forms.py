from django import forms
from .models import NutritionLog, Foods, SleepLog, FitnessLog, Goals, NutritionGoals, FitnessGoals, SleepGoals
from .models import Users, Events, EventParticipants
from django.utils import timezone

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'city', 'state', 'country']
        email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder': 'you@virginia.edu'})
        )
        widgets = {
            'phone_number': forms.TextInput(),
            'city': forms.TextInput(),
            'state': forms.TextInput(),
            'country': forms.TextInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # if not email.endswith('@virginia.edu'):
        #     raise forms.ValidationError("Only @virginia.edu email addresses are allowed.")

        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

class FoodItemForm(forms.ModelForm):

    class Meta:
        model = Foods
        fields = ['food_item', 'food_category', 'per_100_units', 'calories_per_100', 'kj_per_100']
        widgets = {
            'food_item': forms.TextInput(attrs={'placeholder': 'Tomato'}),
            'food_category': forms.TextInput(attrs={'placeholder': 'Fruit'}),
            'per_100_units': forms.TextInput(attrs={'placeholder': 'grams / mL'}),
            'calories_per_100': forms.NumberInput(attrs={'placeholder': '18'}),
            'kj_per_100': forms.NumberInput(attrs={'placeholder': '64'}),
        }

class NutritionLogForm(forms.ModelForm):
    # We don't want to show the time_of_consumption field on the form
    time_of_consumption = forms.DateTimeField(initial=timezone.now, widget=forms.HiddenInput())

    class Meta:
        model = NutritionLog
        fields = ['food', 'num_grams_consumed', 'source', 'description', 'time_of_consumption']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the food dropdown with a queryset from the Foods model
        self.fields['food'].queryset = Foods.objects.all()


class SleepLogForm(forms.ModelForm):
    class Meta:
        model = SleepLog
        fields = ['start_time', 'end_time', 'sleep_quality', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'sleep_quality': forms.TextInput(attrs={'placeholder': '1-10'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional description'}),
        }
        
class FitnessLogForm(forms.ModelForm):
    class Meta:
        model = FitnessLog
        fields = ['activity', 'start_time', 'end_time', 'description']
        widgets = {
            'activity': forms.TextInput(attrs={'placeholder': 'e.g., Running'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'placeholder': 'Optional description'}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goals
        fields = ['goal_type', 'start_time', 'end_time', 'completed', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class NutritionGoalForm(forms.ModelForm):
    class Meta:
        model = NutritionGoals
        fields = ['goal_type', 'start_time', 'end_time', 'completed', 'description', 'food', 'lower_grams', 'upper_grams']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the food dropdown with a queryset from the Foods model
        self.fields['food'].queryset = Foods.objects.all()
class FitnessGoalForm(forms.ModelForm):
    class Meta:
        model = FitnessGoals
        fields = ['goal_type', 'start_time', 'end_time', 'completed', 'description', 'activity', 'target_minutes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class SleepGoalForm(forms.ModelForm):
    class Meta:
        model = SleepGoals
        fields = ['goal_type', 'start_time', 'end_time', 'completed', 'description', 'target_quality', 'target_hours']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['start_time', 'end_time', 'description']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }