from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter,SimpleRouter
router = DefaultRouter()
router.register("building", views.BuildingAPI, basename="building")
router.register("elevator", views.ElevatorAPI, basename="elevator")
router.register("request", views.RequestAPI, basename="request")

urlpatterns = [
    # path('changeDoor',views.Chage)
    path('api/', include(router.urls)),
    path('api/changeDoor/',views.ChangeDoorAPI.as_view(),name="change_door")
]
