# ana urls.py içine ekle
from django.urls import include, path

urlpatterns += [
    path("", include("mission_control.urls")),
    path("customers/", include("customer360.urls")),
]
