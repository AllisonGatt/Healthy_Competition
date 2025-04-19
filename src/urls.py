from django.urls import path
from src import views
from django.contrib.auth import views as auth_views
from .views import profile_view

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log-activity/', views.log_activity, name='log_activity'),
    path("competitions/", views.competition_list, name="competition_list"),
    path("competitions/create/", views.create_competition, name="create_competition"),
    path('competitions/<int:competition_id>/join/', views.join_competition, name='join_competition'),
    path('competition/<int:competition_id>/', views.competition_detail, name='competition_detail'),
]
