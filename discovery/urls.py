from django.urls import path

from . import views

urlpatterns = [
    path('', views.discovery_home, name='discovery_home'),
    path('<int:pk>/', views.discovery_detail, name='discovery_detail'),
    path('<int:pk>/import/', views.discovery_import, name='discovery_import'),
]
