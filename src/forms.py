from django import forms
from .models import ActivityLog

class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = ['steps', 'exercise_type', 'exercise_duration']