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
    
    from django.db import models
from django.contrib.auth.models import User

#model for competitions 
class Competition(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_competitions")
    participants = models.ManyToManyField(User, related_name="joined_competitions", blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    goal_steps = models.IntegerField()

    def __str__(self):
        return self.name

#model for participants in competition
class CompetitionParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField(default=0)
    exercise_minutes = models.PositiveIntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'competition')  #This prevents duplicates

    def __str__(self):
        return f"{self.user.username} in {self.competition.name}"
