from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Building, Elevator, Request
from .serializers import (
    BuildingSerializer,
    ElevatorSerializer,
    RequestSerializer,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_406_NOT_ACCEPTABLE,
)
from django.db.models import Q, Func, F


def check_exist(obj, id):
    obj_list = obj.objects.filter(id=id)
    if obj_list.exists():
        return True, obj_list[0]
    return False, None


class BuildingAPI(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = BuildingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            building = serializer.instance
            for i in range(1, (int(data["no_of_elevators"]) + 1)):
                elevator = Elevator.objects.create(
                    building=building, current_floor=0, elevator_no=i
                )
                elevator.save()
        return Response({"data": serializer.data}, status=200)


class ElevatorAPI(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class RequestAPI(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = RequestSerializer(data=data)
        if serializer.is_valid():
            current_floor = int(data["current_floor"])
            destination_floor = int(data["destination_floor"])
            exist, building = check_exist(Building, data["building"])
            if exist:
                if (
                    current_floor <= building.no_of_floors
                    and destination_floor <= building.no_of_floors
                ):
                    if current_floor < destination_floor:
                        direction = "up"
                    else:
                        direction = "down"
                    elevators = Elevator.objects.filter(working_status="working")
                    if direction == "up":
                        elevators_fi = elevators.filter(
                            Q(status=direction) & Q(current_floor__lte=current_floor)
                        )
                    else:
                        elevators_fi = elevators.filter(
                            Q(status=direction) & Q(current_floor__gte=current_floor)
                        )

                    if not elevators_fi.exists():
                        elevators_fi = elevators.filter(status="stoped")

                    elevator = (
                        elevators_fi.annotate(
                            abs_diffrance=Func(
                                F("current_floor") - current_floor,
                                function="ABS",
                            )
                        )
                        .order_by("abs_diffrance")
                        .first()
                    )
                    if elevator is None:
                        user_requests = Request.objects.filter(status="ongoing")
                        closest_request = (
                            user_requests.annotate(
                                abs_diffrance=Func(
                                    F("destination_floor") - current_floor,
                                    function="ABS",
                                )
                            )
                            .order_by("abs_diffrance")
                            .first()
                        )
                        elevator = closest_request.elevator
                    serializer.save()
                    serializer.instance.direction = direction
                    serializer.instance.elevator = elevator
                    serializer.instance.save()
                    elevator.status = direction
                    elevator.save()
                return Response(
                    {
                        "status": 406,
                        "message": f"Current floors or Destination floors must be less than  {building.no_of_floors} ",
                    },
                    status=HTTP_406_NOT_ACCEPTABLE,
                )
            return Response(
                {
                    "status": 406,
                    "message": "Enter valid building id",
                },
                status=HTTP_406_NOT_ACCEPTABLE,
            )
            return Response(data=serializer.data, status=HTTP_200_OK)
        return Response(
            {
                "status": 406,
                "message": "id is required",
            },
            status=HTTP_406_NOT_ACCEPTABLE,
        )


class ChangeDoorAPI(APIView):
    def patch(self, request):
        data = request.data
        if data["id"] is not None:
            try:
                id = int(data["id"])
                elevator = Elevator.objects.get(id=id)
                if elevator.door_status == "open":
                    elevator.door_status = "close"
                else:
                    elevator.door_status = "open"
                elevator.save()
                serializer = ElevatorSerializer(elevator)

                return Response(
                    {
                        "status": 200,
                        "message": "door status changed successfully",
                        "data": serializer.data,
                    },
                    status=HTTP_200_OK,
                )
            except Exception:
                return Response(
                    {
                        "status": 406,
                        "message": "id must be an integer",
                    },
                    status=HTTP_406_NOT_ACCEPTABLE,
                )
        return Response(
            {
                "status": 406,
                "message": "id is required",
            },
            status=HTTP_406_NOT_ACCEPTABLE,
        )
