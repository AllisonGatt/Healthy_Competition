from django.urls import path
from src import views

urlpatterns = [
    path("", views.home, name="home"),
]
