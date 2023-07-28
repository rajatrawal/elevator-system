from django.shortcuts import render
from rest_framework.views import APIView
from .models import Building, Floor, Elevator
from .serializers import BuildingSerializer, ElevatorSerializer
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


def check_exist(obj, id):
    obj_list = obj.objects.filter(id=id)
    if obj_list.exists():
        return True, obj_list[0]
    return False, None


class BuildingAPI(APIView):
    def get(self, request):
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = BuildingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                building = Building.objects.get(id=serializer.data["id"])
                floor_0 = None
                for i in range(serializer.data["no_of_floors"] + 1):
                    floor = Floor.objects.create(number=i, building=building)
                    floor.save()
                    if i == 0:
                        floor_0 = floor
                for i in range(1, (serializer.data["no_of_elevators"] + 1)):
                    print(floor_0)
                    elevator = Elevator.objects.create(
                        building=building, current_floor=floor_0, elevator_no=i
                    )
                    elevator.save()
                return Response(
                    {
                        "status": 200,
                        "message": "Building and its Elevators and Floors are created successfully",
                        "data": serializer.data,
                    },
                    status=HTTP_200_OK,
                )
            return Response(
                {"status": 406, "message": "Invalid  Data", "error": serializer.errors},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        except Exception:
            return Response(
                {
                    "status": 400,
                    "message": "Invalid Request",
                },
                status=HTTP_400_BAD_REQUEST,
            )


class ElevatorAPI(APIView):
    def get(self, request):
        elevator = Elevator.objects.all()
        serializer = ElevatorSerializer(elevator, many=True)
        return Response(
            data={"status": 200, "data": serializer.data},
            status=HTTP_200_OK,
        )

    def patch(self, request):
        data = request.data
        elevator_id = data["id"]
        if elevator_id is not None:
            is_exist, elevator = check_exist(Elevator, elevator_id)
        if is_exist is False or elevator_id is None:
            return Response(
                {
                    "status": 422,
                    "message": "Elevator not exist. Please give valid data",
                },
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )
        elif is_exist is True:
            serializer = ElevatorSerializer(elevator, data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": 200,
                        "message": "Elevator Data updated successfully.",
                        "data": serializer.data,
                    },
                    status=HTTP_200_OK,
                )
            return Response(
                {"status": 406, "message": "Invalid  Data", "error": serializer.errors},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
