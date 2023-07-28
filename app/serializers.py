from rest_framework import serializers
from .models import Building,Elevator,Floor,Request

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        exclude = ('id','created_at','updated_at','building')

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        exclude=('created_at','updated_at')
        
class ElevatorSerializer(serializers.ModelSerializer):
    current_floor = FloorSerializer(read_only=True)
    building = BuildingSerializer(read_only=True)
    class Meta:
        model = Elevator
        exclude = ('created_at','updated_at')
        
        