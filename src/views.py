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
        if form.is_valid():
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
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            
            # Update user's profile stats
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.steps_logged += activity.steps
            profile.exercises_logged += 1
            profile.save()

            return redirect('dashboard')
    else:
        form = ActivityLogForm()
    
    return render(request, 'log_activity.html', {'form': form})

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    activities = ActivityLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'profile.html', {'profile': profile, 'activities': activities})

#GET RID OF IF NOT NEEDED
# @login_required
# def profile_view(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)  # Create if missing
#     return render(request, 'profile.html', {'profile': profile})