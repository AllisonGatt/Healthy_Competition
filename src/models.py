from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #one to one so that each user only has one profile
    bio = models.TextField(blank=True, null=True) #optional text 
    steps_logged = models.IntegerField(default=0) #default zero, steps logged, integer
    exercises_logged = models.IntegerField(default=0) #default zero, exercise, integer

#profile object is represented as a string
    def __str__(self):
        return f"{self.user.username}'s Profile"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #links to Django's User model
    date = models.DateField(auto_now_add=True) #records when data is logged
    steps = models.IntegerField() #stores the steps as an integer
    exercise_type = models.CharField(max_length=100) #short text, no more than 100 characters
    exercise_duration = models.IntegerField(help_text="Duration in minutes") #integer for minutes

    def __str__(self):
        return f"{self.user.username} - {self.date}"