from django import forms
from .models import ActivityLog
from .models import Competition

class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ['steps', 'exercise_type', 'exercise_duration']

#form for competiton
class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ["name", "start_date", "end_date", "goal_steps"]