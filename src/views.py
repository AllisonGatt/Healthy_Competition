from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, Case, When, IntegerField
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


from .models import Profile, ActivityLog
from .models import ActivityLog, Profile
from .models import Competition, CompetitionParticipant

from .forms import ActivityLogForm
from .forms import CompetitionForm

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

# @login_required
# def log_activity(request):
#     if request.method == 'POST':
#         form = ActivityLogForm(request.POST)
#         if form.is_valid():
#             activity = form.save(commit=False)
#             activity.user = request.user

#             if activity.activity_type == 'steps' and activity.steps == 0:
#                 form.add_error('steps', 'Please enter the number of steps.')
#             elif activity.activity_type == 'exercise' and activity.minutes == 0:
#                 form.add_error('minutes', 'Please enter the number of minutes.')
#             else:
#                 activity.save()

#                 # Update profile
#                 profile, created = Profile.objects.get_or_create(user=request.user)
#                 if activity.activity_type == 'steps':
#                     profile.steps_logged += activity.steps
#                 elif activity.activity_type == 'exercise':
#                     profile.exercises_logged += 1
#                 profile.save()

#                 today = timezone.now().date()
#                 active_competitions = Competition.objects.filter(
#                     competitionparticipant__user=request.user,
#                     competition_type=activity.activity_type,
#                     start_date__lte=today,
#                     end_date__gte=today
#                 )

#                 for competition in active_competitions:
#                     participant = CompetitionParticipant.objects.get(
#                         user=request.user, competition=competition
#                     )
#                     if activity.activity_type == 'steps':
#                         participant.progress += activity.steps
#                     elif activity.activity_type == 'exercise':
#                         participant.progress += activity.minutes
#                     participant.save()


#                 return redirect('dashboard')
#     else:
#         form = ActivityLogForm()

#     return render(request, 'log_activity.html', {'form': form})


#profile view, shows the exercise/steps logged and the date logged
#uses sum to give total steps per date with a default of 0
#orders by date
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    daily_activity = (
        ActivityLog.objects
        .filter(user=request.user)
        .values('date')  # Use date directly, since it's already a DateField
        .annotate(
            total_steps=Sum(
                Case(
                    When(activity_type='steps', then='steps'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            total_minutes=Sum(
                Case(
                    When(activity_type='exercise', then='minutes'),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        .order_by('-date')
    )

    logs = ActivityLog.objects.filter(user=request.user).order_by('-date')

    return render(request, 'profile.html', {
        'profile': profile,
        'daily_activity': daily_activity,
        'logs': logs,
    })

@login_required
@require_http_methods(["POST"])
def log_activity_ajax(request):
    form = ActivityLogForm(request.POST)
    if form.is_valid():
        activity = form.save(commit=False)
        activity.user = request.user

        # Extra validation
        if activity.activity_type == 'steps' and activity.steps == 0:
            return JsonResponse({'status': 'error', 'errors': {'steps': ['Please enter the number of steps.']}})
        if activity.activity_type == 'exercise' and activity.minutes == 0:
            return JsonResponse({'status': 'error', 'errors': {'minutes': ['Please enter the number of minutes.']}})

        activity.save()

        # Update profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        if activity.activity_type == 'steps':
            profile.steps_logged += activity.steps
        elif activity.activity_type == 'exercise':
            profile.exercises_logged += 1
        profile.save()

        # Update competition progress
        today = timezone.now().date()
        active_competitions = Competition.objects.filter(
            competitionparticipant__user=request.user,
            competition_type=activity.activity_type,
            start_date__lte=today,
            end_date__gte=today
        )

        for competition in active_competitions:
            participant = CompetitionParticipant.objects.get(
                user=request.user, competition=competition
            )
            if activity.activity_type == 'steps':
                participant.progress += activity.steps
            elif activity.activity_type == 'exercise':
                participant.progress += activity.minutes
            participant.save()

        # Render updated rows
        row_html = render_to_string('partials/activity_list_item.html', {'activity': activity})
        profile_row_html = render_to_string('partials/activity_table_row.html', {'log': activity})

        return JsonResponse({
            'status': 'success',
            'row_html': row_html,
            'profile_row_html': profile_row_html
        })

    # If invalid form
    return JsonResponse({'status': 'error', 'errors': form.errors})


#view to edit activities 
@login_required
def edit_activity(request, pk):
    activity = get_object_or_404(ActivityLog, pk=pk, user=request.user) #calls on ActivityLog model
    if request.method == 'POST':
        form = ActivityLogForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ActivityLogForm(instance=activity)
    return render(request, 'edit_activity.html', {'form': form})

#view to delete activities
@login_required
def delete_activity(request, pk):
    activity = get_object_or_404(ActivityLog, pk=pk, user=request.user)
    if request.method == 'POST':
        activity.delete()
        return redirect('profile')
    return render(request, 'delete_activity.html', {'activity': activity})

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

    # Get IDs of competitions the current user joined
    joined_comp_ids = CompetitionParticipant.objects.filter(user=request.user).values_list('competition_id', flat=True)

    return render(request, 'competition_list.html', {
        'current_competitions_steps': current_competitions_steps,
        'current_competitions_minutes': current_competitions_minutes,
        'past_competitions_steps': past_competitions_steps,
        'past_competitions_minutes': past_competitions_minutes,
        'joined_comp_ids': joined_comp_ids
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
            #steps=0  
            progress=0
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
    #participants = CompetitionParticipant.objects.filter(competition=competition).order_by('-steps')
    
    # Determine what to sort by
    # if competition.competition_type == 'steps':
    #     participants = participants.order_by('-steps')
    # elif competition.competition_type == 'minutes':
    #     participants = participants.order_by('-exercise_minutes')

    participants = CompetitionParticipant.objects.filter(competition=competition).order_by('-progress')

    
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
