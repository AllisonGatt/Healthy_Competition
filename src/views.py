from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, ActivityLog
from .forms import ActivityLogForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Competition
from .forms import CompetitionForm
from django.shortcuts import get_object_or_404
from .models import Competition, CompetitionParticipant

from django.contrib.auth.decorators import login_required
from .models import Competition, CompetitionParticipant
from django.contrib import messages
from django.utils import timezone

from .models import Competition, CompetitionParticipant


def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid(): #ensures the input data is valid
            user = form.save()
            login(request, user)  # Automatically log in the new user
            return redirect("index")  # Redirect to the homepage or dashboard
    else:
        form = UserCreationForm()
    
    return render(request, "signup.html", {"form": form})

@login_required
def dashboard(request):
    activities = ActivityLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard.html', {'activities': activities})

@login_required
def log_activity(request):
    if request.method == 'POST':
        form = ActivityLogForm(request.POST) #POST method, sending data
        if form.is_valid():
            activity = form.save(commit=False) #does not save yet, creates an instance 
            activity.user = request.user #this assigns the current user
            activity.save() #this saves to the SQLite database
            
            # Update user's profile stats
            profile, created = Profile.objects.get_or_create(user=request.user) #makes sure user has profile
            profile.steps_logged += activity.steps #this adds new steps
            profile.exercises_logged += 1 #This increments the exercise count
            profile.save() #saves 

            return redirect('dashboard') #returns to dashboard 
    else:
        form = ActivityLogForm()
    
    return render(request, 'log_activity.html', {'form': form})

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user) #fetches logged in user's profile 
    activities = ActivityLog.objects.filter(user=request.user).order_by('-date') #shows activity log by date
    return render(request, 'profile.html', {'profile': profile, 'activities': activities})

#creating a competition list
@login_required
def competition_list(request):
    today = timezone.now().date()
    all_competitions = Competition.objects.all()

    current_competitions_steps = all_competitions.filter(
        competition_type='steps',
        end_date__gte=today
    )

    current_competitions_minutes = all_competitions.filter(
        competition_type='minutes',
        end_date__gte=today
    )

    past_competitions_steps = all_competitions.filter(
        competition_type='steps',
        end_date__lt=today
    )

    past_competitions_minutes = all_competitions.filter(
        competition_type='minutes',
        end_date__lt=today
    )

    return render(request, 'competition_list.html', {
        'current_competitions_steps': current_competitions_steps,
        'current_competitions_minutes': current_competitions_minutes,
        'past_competitions_steps': past_competitions_steps,
        'past_competitions_minutes': past_competitions_minutes
    })


#creating a competition
@login_required
def create_competition(request):
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.creator = request.user
            competition.save()
            competition.participants.add(request.user)
            return redirect("competition_list")
    else:
        form = CompetitionForm()
    return render(request, "create_competition.html", {"form": form})

#joining a competition
@login_required
def join_competition(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)

    #checks to make sure the user is not already a participant  
    already_joined = CompetitionParticipant.objects.filter(
        user=request.user, competition=competition
    ).exists()
    
    if not already_joined:
        CompetitionParticipant.objects.create(
            user=request.user,
            competition=competition,
            steps=0  
        )
        messages.success(request, f"You joined the competition: {competition.name}")
    else:
        messages.info(request, f"You already joined {competition.name}")
    
    return redirect('competition_detail', competition_id=competition.id)

def competition_detail(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    participants = CompetitionParticipant.objects.filter(competition=competition)
    return render(request, 'competition_detail.html', {
        'competition': competition,
        'participants': participants
    })


def competition_results(request, competition_id):
    competition = get_object_or_404(Competition, id=competition_id)
    participants = CompetitionParticipant.objects.filter(competition=competition).order_by('-steps')
    
    # Determine what to sort by
    if competition.competition_type == 'steps':
        participants = participants.order_by('-steps')
    elif competition.competition_type == 'minutes':
        participants = participants.order_by('-exercise_minutes')
    
    # Leaderboard and user rank
    leaderboard = list(participants)
    user_participant = participants.filter(user=request.user).first()
    user_rank = None

    if user_participant:
        for index, participant in enumerate(leaderboard):
            if participant.user == request.user:
                user_rank = index + 1
                break

    return render(request, 'competition_results.html', {
        'competition': competition,
        'leaderboard': leaderboard,
        'user_participant': user_participant,
        'user_rank': user_rank
    })
