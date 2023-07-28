from typing import Iterable, Optional
from django.db import models
from uuid import uuid4


# base model to follow DRY principle
class BaseModel(models.Model):
    # uuid field to differentiate each model
    id = models.UUIDField(default=uuid4, primary_key=True, null=False, blank=False)
    # datetime field when the object was created
    created_at = models.DateTimeField(auto_now_add=True)
    # datetime field when the object was updated last time
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# A specific building
class Building(BaseModel):
    # name of buliding
    name = models.CharField(max_length=200, null=False, blank=False)
    # numbers of floors in buliding
    no_of_floors = models.IntegerField(blank=False, null=False)
    # numbers of elevators in buliding
    no_of_elevators = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return self.name

# Floor for a specific building
class Floor(BaseModel):
    # Floor number
    number = models.IntegerField(blank=False, null=False)
    building = models.ForeignKey(
        Building, blank=True, null=True, related_name="floors", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.building.name} {self.number}"


# An elevator object
class Elevator(BaseModel):
    choices = (("available", "available"), ("up", "up"), ("down", "down"))
    # A forgein key to specity elevator of building
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name="elevator"
    )
    # status of elevator
    status = models.CharField(choices=choices, max_length=10, default="available")
    # door status of elevator
    door_status = models.CharField(
        choices=(("open", "open"), ("closed", "closed")), max_length=6,default='closed'
    )
    # working status of elevator in bool
    is_working = models.BooleanField(default=True)
    #current floor of elevator
    current_floor = models.ForeignKey(
        Floor, on_delete=models.CASCADE, related_name="elevators",default=None
    )
    elevator_no = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.building.name} {self.elevator_no} {self.status} "





# Request model to store data
class Request(BaseModel):
    choices = (("up", "up"), ("down", "down"))
    # direction on elevator for that request
    direction = models.CharField(choices=choices, blank=True, null=True, max_length=4)
    # floor from which request is send
    current_floor = models.ForeignKey(
        Floor, on_delete=models.CASCADE, related_name="requests"
    )
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name="requests"
    )
    # destination floor
    destination_floors = models.ManyToManyField(Floor)
    elevator = models.ForeignKey(
        Elevator,
        blank=True,
        null=True,
        related_name="requests",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.building.name} {self.elevator} {self.direction}"
