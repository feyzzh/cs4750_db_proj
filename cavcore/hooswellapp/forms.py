from django import forms
from .models import NutritionLog, Foods
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
