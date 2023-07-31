from rest_framework import serializers
from .models import Building, Elevator, Request
from action_serializer import ModelActionSerializer

# here using actioni-serializer package to use ModelActionSerializer features it allows to show and hide models fields


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        exclude = ("created_at", "updated_at")


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        exclude = ("created_at", "updated_at")


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        exclude = ("created_at", "updated_at")
