from django import forms
from .models import ActivityLog
from .models import Competition
from django.utils import timezone

class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ['steps', 'date']
        widgets = {
            'steps': forms.NumberInput(attrs={'placeholder': 'Enter step count'}),
            'date': forms.DateInput(attrs={'type': 'date'})  # HTML5 date picker
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > timezone.now().date():
            raise forms.ValidationError("You cannot log steps for a future date.")
        return date

    def __init__(self, *args, **kwargs):
        super(ActivityLogForm, self).__init__(*args, **kwargs)
        self.fields['steps'].required = False
        self.fields['date'].required = True
        
#form for competiton
class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'start_date', 'end_date']
        widgets = { #added widgets for easier dates
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }