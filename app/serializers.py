from rest_framework import serializers
from .models import Building, Elevator, Request
from action_serializer import ModelActionSerializer

# here using actioni-serializer package to use ModelActionSerializer features it allows to show and hide models fields


class BuildingSerializer(ModelActionSerializer):
    class Meta:
        model = Building
        exclude = ("id", "created_at", "updated_at")

        action_fields = {
            "list": {"fields": ("id", "name", "no_of_floors", "no_of_elevators")}
        }


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        exclude = ("id", "created_at", "updated_at")


class RequestSerializer(ModelActionSerializer):
    class Meta:
        model = Request
        exclude = ("id", "created_at", "updated_at", "status", "direction", "elevator")
        action_fields = {
            "list": {
                "fields": (
                    "id",
                    "status",
                    "direction",
                    "elevator",
                    "current_floor",
                    "destination_floor",
                    "building",
                )
            }
        }
