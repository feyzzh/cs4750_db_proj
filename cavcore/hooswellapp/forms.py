from django import forms
from .models import NutritionLog, Foods, SleepLog, FitnessLog
from django.utils import timezone

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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['end_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

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