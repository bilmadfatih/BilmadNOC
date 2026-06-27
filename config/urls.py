from django.contrib import admin
from django.urls import path
from core import views as core_views

urlpatterns = [
    path('', core_views.dashboard, name='dashboard'),
    path('noc-wall/', core_views.noc_wall, name='noc_wall'),
    path('security-wall/', core_views.security_wall, name='security_wall'),
    path('companies/', core_views.company_list, name='company_list'),
    path('admin/', admin.site.urls),
]
