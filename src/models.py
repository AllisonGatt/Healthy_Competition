from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #one to one so that each user only has one profile
    bio = models.TextField(blank=True, null=True) #optional text 
    steps_logged = models.IntegerField(default=0) #default zero, steps logged, integer

#profile object is represented as a string
    def __str__(self):
        return f"{self.user.username}'s Profile"

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField(default=0)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

#model for competitions 
class Competition(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_competitions")
    participants = models.ManyToManyField(User, related_name="joined_competitions", blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

#model for participants in competition
class CompetitionParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField(default=0)  
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'competition')  #This prevents duplicates

    def __str__(self):
        return f"{self.user.username} in {self.competition.name}"
