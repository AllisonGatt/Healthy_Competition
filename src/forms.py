from django import forms
from .models import ActivityLog
from .models import Competition

class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ['steps']
        widgets = {
            'steps': forms.NumberInput(attrs={'placeholder': 'Enter step count'}),
            # 'minutes': forms.NumberInput(attrs={'placeholder': 'Enter minutes exercised'}),
        }

    def __init__(self, *args, **kwargs):
        super(ActivityLogForm, self).__init__(*args, **kwargs)
        self.fields['steps'].required = False
        # self.fields['minutes'].required = False
        
#form for competiton
class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'start_date', 'end_date']
        widgets = { #added widgets for easier dates
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }