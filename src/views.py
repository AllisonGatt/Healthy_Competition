from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, ActivityLog
from .forms import ActivityLogForm


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

