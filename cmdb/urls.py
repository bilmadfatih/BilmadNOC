from django.urls import path
from . import views

urlpatterns = [
    path('', views.cmdb_overview, name='cmdb_overview'),
]
