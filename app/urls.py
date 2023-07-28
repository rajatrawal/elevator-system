from django.urls import path
from . import views

urlpatterns = [
    path("api/building/", views.BuildingAPI.as_view(), name="building"),
    path("api/elevator/", views.ElevatorAPI.as_view(), name="elevator"),
]
