from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    steps_logged = models.IntegerField(default=0)
    exercises_logged = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    steps = models.IntegerField()
    exercise_type = models.CharField(max_length=100)
    exercise_duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return f"{self.user.username} - {self.date}"