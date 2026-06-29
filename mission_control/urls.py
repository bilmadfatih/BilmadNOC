from django.urls import path
from . import views

app_name = "mission_control"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
